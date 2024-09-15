import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import DATABASE_URL

async_engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession

)


class Base(DeclarativeBase):
    pass


logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
