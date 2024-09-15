import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from src.user.model import User
from src.user.schema import UserCreate
from src.utils.password_hashing import hash_password

logger = logging.getLogger(__name__)


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        hashed_password=hashed_password
    )

    session.add(db_user)

    try:
        await session.commit()
        await session.refresh(db_user)
        logger.info(f"User created successfully: {user.username}")
    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Integrity error while creating user: {e}")
        raise HTTPException(status_code=400, detail="User already exists")
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"SQLAlchemy error while creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        await session.rollback()
        logger.error(f"Unexpected error while creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return db_user


async def get_user_by_username(session: AsyncSession, username: str) -> User or None:
    try:
        result = await session.execute(select(User).filter(User.username == username))
        user = result.scalars().first()
        if user is None:
            logger.info(f"User not found by username: {username}")
        else:
            logger.info(f"User retrieved by username: {username}")
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error while retrieving user by username: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.error(f"Unexpected error while retrieving user by username: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User or None:
    try:
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if user is None:
            logger.info(f"User not found by id: {user_id}")
        else:
            logger.info(f"User retrieved by id: {user_id}")
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error while retrieving user by id: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.error(f"Unexpected error while retrieving user by id: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return user
