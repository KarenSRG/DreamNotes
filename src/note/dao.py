import logging

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Depends

from src.database import get_db
from src.logging_config import logger
from src.note.model import Note
from src.note.schema import NoteCreate, NoteUpdate
from src.user.schema import UserResponse


async def create_note(
        session: AsyncSession,
        note: NoteCreate,
        user: UserResponse
) -> Note:
    db_note = Note(
        title=note.title,
        content=note.content,
        tags=','.join(note.tags) if note.tags else '',
        owner_id=user.id
    )

    session.add(db_note)

    try:
        await session.commit()
        await session.refresh(db_note)
        logger.info(f"Note created with ID: {db_note.id} by user ID: {user.id}")
    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Integrity error while creating note: {e}")
        raise HTTPException(status_code=400, detail="Integrity Error")
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"SQLAlchemy error while creating note: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        await session.rollback()
        logger.error(f"Unexpected error while creating note: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return db_note


async def get_note_by_id(
        session: AsyncSession,
        note_id: int,
        user: UserResponse

) -> Note:
    try:
        result = await session.execute(select(Note).filter(Note.id == note_id, Note.owner_id == user.id))
        note = result.scalars().first()
        if note is None:
            logger.warning(f"Note with ID: {note_id} not found for user ID: {user.id}")
            raise HTTPException(status_code=404, detail="Note not found")
        logger.info(f"Note retrieved with ID: {note_id} by user ID: {user.id}")
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error while retrieving note: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return note


async def get_notes_by_tags(
        session: AsyncSession,
        owner_id: int,
        prompt: str,
        skip: int = 0,
        limit: int = 10,

) -> list[Note]:
    try:
        print(prompt)
        result = await session.execute(
            select(Note).filter(
                and_(
                    Note.owner_id == owner_id,
                    Note.tags.ilike(f'%,{prompt},%') |
                    Note.tags.ilike(f'{prompt},%') |
                    Note.tags.ilike(f'%,{prompt}') |
                    Note.tags.ilike(f'{prompt}')
                )
            ).offset(skip).limit(limit))

        notes = result.scalars().all()
        logger.info(f"Retrieved {len(notes)} notes for user ID: {owner_id}")
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error while retrieving notes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return notes


async def get_notes_by_owner(
        session: AsyncSession,
        owner_id: int,
        skip: int = 0,
        limit: int = 10,

) -> list[Note]:
    try:
        result = await session.execute(select(Note).filter(Note.owner_id == owner_id).offset(skip).limit(limit))
        notes = result.scalars().all()
        logger.info(f"Retrieved {len(notes)} notes for user ID: {owner_id}")
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error while retrieving notes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return notes


async def update_note(
        session: AsyncSession,
        note_id: int,
        note_update: NoteUpdate,
        user: UserResponse

) -> Note:
    try:
        result = await session.execute(
            select(Note).filter(
                Note.id == note_id,
                Note.owner_id == user.id)
        )
        db_note = result.scalars().first()
        if db_note is None:
            logger.warning(f"Note with ID: {note_id} not found for user ID: {user.id}")
            await session.rollback()
            raise HTTPException(status_code=404, detail="Note not found")
        for var, value in vars(note_update).items():
            setattr(db_note, var, value) if value is not None else None
        session.add(db_note)
        await session.commit()
        await session.refresh(db_note)
        logger.info(f"Note updated with ID: {note_id} by user ID: {user.id}")
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"SQLAlchemy error while updating note: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return db_note


async def delete_note(
        session: AsyncSession,
        note_id: int,
        user: UserResponse

) -> None:
    try:

        result = await session.execute(
            select(Note).filter(
                Note.id == note_id,
                Note.owner_id == user.id)
        )

        db_note = result.scalars().first()

        if db_note is None:
            logger.warning(f"Note with ID: {note_id} not found for user ID: {user.id}")
            raise HTTPException(status_code=404, detail="Note not found")

        await session.delete(db_note)
        await session.commit()

        logger.info(f"Note deleted with ID: {note_id} by user ID: {user.id}")

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"SQLAlchemy error while deleting note: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
