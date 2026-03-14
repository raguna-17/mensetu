from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os


# 環境変数からDB URL取得
DATABASE_URL = os.getenv("DATABASE_URL")

# 非同期エンジン作成
engine = create_async_engine(DATABASE_URL, echo=False)

# 非同期セッション作成
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

# FastAPI依存関係用
async def get_db():
    async with async_session() as session:
        yield session