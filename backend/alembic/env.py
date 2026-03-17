import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.models import Base  # 縺薙％縺ｫ蜈ｨ繝｢繝・Ν縺ｮ Base 繧偵う繝ｳ繝昴・繝・
config = context.config

# Logging 險ｭ螳・fileConfig(config.config_file_name)

DATABASE_URL = os.getenv("DATABASE_URL")


# 繧ｪ繝輔Λ繧､繝ｳ繝｢繝ｼ繝・def run_migrations_offline():
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# 蜷梧悄髢｢謨ｰ縺ｨ縺励※ Alembic 繝槭う繧ｰ繝ｬ繝ｼ繧ｷ繝ｧ繝ｳ蜃ｦ逅・ｒ螳夂ｾｩ
def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        compare_type=True,  # 蝙九・螟画峩繧よ､懷・
    )
    with context.begin_transaction():
        context.run_migrations()


# 繧ｪ繝ｳ繝ｩ繧､繝ｳ繝｢繝ｼ繝会ｼ磯撼蜷梧悄 DB 謗･邯夲ｼ・async def run_migrations_online():
    connectable = async_engine_from_config(
        {"sqlalchemy.url": DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        # 髱槫酔譛溘お繝ｳ繧ｸ繝ｳ縺縺代←繝槭う繧ｰ繝ｬ繝ｼ繧ｷ繝ｧ繝ｳ蜃ｦ逅・・菴薙・蜷梧悄髢｢謨ｰ繧剃ｽｿ縺・        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

