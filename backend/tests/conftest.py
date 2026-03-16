import os
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import get_db
from app.models import User, Company, Application
from app.auth import create_access_token
from argon2 import PasswordHasher

ph = PasswordHasher()

DATABASE_URL = os.getenv("DATABASE_URL")

AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(DATABASE_URL)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture
async def db_session(engine):
    async with engine.connect() as connection:
        transaction = await connection.begin()

        session = AsyncSessionLocal(bind=connection)

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()



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
async def test_user(db_session):

    user = User(
        email="test@example.com",
        hashed_password=ph.hash("password"),
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest.fixture
async def test_company(db_session):

    company = Company(
        name="Test Company",
        industry="IT"
    )

    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)

    return company


@pytest.fixture
async def test_application(db_session, test_user, test_company):

    application = Application(
        position="Backend Engineer",
        user_id=test_user.id,
        company_id=test_company.id
    )

    db_session.add(application)
    await db_session.commit()
    await db_session.refresh(application)

    return application


@pytest.fixture
async def auth_headers(test_user):

    token = create_access_token({"sub": str(test_user.id)})

    return {
        "Authorization": f"Bearer {token}"
    }