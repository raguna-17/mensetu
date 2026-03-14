from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
async_session = None

Base = declarative_base()


def get_engine():
    global engine

    if engine is None:
        engine = create_async_engine(DATABASE_URL, echo=False)

    return engine


def get_sessionmaker():
    global async_session

    if async_session is None:
        async_session = async_sessionmaker(
            get_engine(),
            expire_on_commit=False,
            class_=AsyncSession,
        )

    return async_session


async def get_db():

    sessionmaker = get_sessionmaker()

    async with sessionmaker() as session:
        yield session