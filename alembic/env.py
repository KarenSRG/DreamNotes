from alembic import context
from sqlalchemy import create_engine

from src.config import DATABASE_URL
from src.database import Base

engine = create_engine(DATABASE_URL)


def run_migrations_online():
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            literal_binds=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()
