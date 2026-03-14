import os
import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from alembic import command
from alembic.config import Config

from app.main import app
from app.db import get_db, get_sessionmaker


# -----------------------------
# DATABASE
# -----------------------------

DATABASE_URL = os.getenv("DATABASE_URL")


# -----------------------------
# Run Alembic migration
# -----------------------------

@pytest.fixture(scope="session", autouse=True)
def run_migrations():

    sync_url = DATABASE_URL.replace("+asyncpg", "")

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url)

    command.upgrade(alembic_cfg, "head")


# -----------------------------
# DB Session
# -----------------------------

@pytest_asyncio.fixture
async def db_session():

    sessionmaker = get_sessionmaker()

    async with sessionmaker() as session:
        yield session
        await session.rollback()


# -----------------------------
# Test client
# -----------------------------

@pytest_asyncio.fixture
async def client(db_session):

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# -----------------------------
# Auth client
# -----------------------------

@pytest_asyncio.fixture
async def auth_client(client):

    user = {
        "email": "test@example.com",
        "password": "password123",
    }

    await client.post("/api/v1/users/register", json=user)

    res = await client.post("/api/v1/users/login", json=user)

    token = res.json()["access_token"]

    client.headers.update(
        {"Authorization": f"Bearer {token}"}
    )

    return client