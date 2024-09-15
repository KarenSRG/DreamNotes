# alembic/env.py

from __future__ import annotations
import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

app_path = Path(__file__).resolve().parent.parent / 'app'
sys.path.insert(0, str(app_path))

from app.config import DATABASE_URL
from app.database import Base
from app.models import User, Note

target_metadata = Base.metadata


def run_migrations_online():
    connectable = engine_from_config(
        {
            "sqlalchemy.url": DATABASE_URL
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
