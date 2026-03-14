import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.models import Base  # ここに全モデルの Base をインポート

config = context.config

# Logging 設定
fileConfig(config.config_file_name)

DATABASE_URL = os.getenv("DATABASE_URL")


# オフラインモード
def run_migrations_offline():
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# 同期関数として Alembic マイグレーション処理を定義
def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        compare_type=True,  # 型の変更も検出
    )
    with context.begin_transaction():
        context.run_migrations()


# オンラインモード（非同期 DB 接続）
async def run_migrations_online():
    connectable = async_engine_from_config(
        {"sqlalchemy.url": DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        # 非同期エンジンだけどマイグレーション処理自体は同期関数を使う
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())