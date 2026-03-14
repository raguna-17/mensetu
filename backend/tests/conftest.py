import asyncio
import os
import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config

from app.main import app
from app.db import get_db

# -----------------------------
# CI用 DATABASE
# -----------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# -----------------------------
# Event loop
# -----------------------------

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# -----------------------------
# Engine
# -----------------------------

@pytest.fixture(scope="session")
async def engine():

    engine = create_async_engine(
        DATABASE_URL,
        future=True,
        echo=False
    )

    yield engine

    await engine.dispose()

# -----------------------------
# Alembic migration
# -----------------------------

@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    """
    CI開始時にAlembic migrationを実行
    """

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

# -----------------------------
# DB Session
# -----------------------------

@pytest.fixture
async def db_session(engine):

    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()

# -----------------------------
# Dependency override
# -----------------------------

@pytest.fixture
async def client(db_session):

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()



@pytest.fixture
async def auth_client(client):

    user = {
        "email": "test@example.com",
        "password": "password123"
    }

    await client.post("/api/v1/users/register", json=user)

    res = await client.post("/api/v1/users/login", json=user)

    token = res.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client