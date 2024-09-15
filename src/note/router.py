from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import REQUEST_LIMIT_PER_MINUTE as rl_tms

from src.database import get_db
from src.note.schema import NoteCreate, NoteUpdate, NoteResponse
from src.note import dao
from src.user.auth import get_current_user
from src.user.model import User

router = APIRouter()


@router.post(
    "/notes/",
    response_model=NoteResponse,
    dependencies=[Depends(RateLimiter(times=rl_tms, seconds=60))]
)
async def create_note(
        note: NoteCreate,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
) -> NoteResponse:
    db_note = await dao.create_note(session, note, user)
    db_note.tags = note.tags
    return db_note


@router.get(
    "/notes/",
    response_model=List[NoteResponse],
    dependencies=[Depends(RateLimiter(times=rl_tms, seconds=60))]
)
async def read_notes(
        skip: int = 0,
        limit: int = 10,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
) -> List[NoteResponse]:
    notes = await dao.get_notes_by_owner(session, user.id, skip, limit)
    for note in notes:
        note.tags = note.tags.split(",") if note.tags else []
    return notes


@router.get(
    "/notes/{prompt}",
    response_model=List[NoteResponse],
    dependencies=[Depends(RateLimiter(times=rl_tms, seconds=60))]
)
async def read_notes_by_tag(
        prompt: str,
        skip: int = 0,
        limit: int = 10,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
) -> List[NoteResponse]:
    notes = await dao.get_notes_by_tags(session, user.id, prompt, skip, limit)

    for note in notes:
        note.tags = note.tags.split(",") if note.tags else []

    return notes


@router.get(
    "/notes/{note_id}",
    response_model=NoteResponse,
    dependencies=[Depends(RateLimiter(times=rl_tms, seconds=60))]
)
async def read_note(
        note_id: int,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
) -> NoteResponse:
    note = await dao.get_note_by_id(session, note_id, user)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note.tags = note.tags.split(",") if note.tags else []
    return note


@router.put(
    "/notes/{note_id}",
    response_model=NoteResponse,
    dependencies=[Depends(RateLimiter(times=rl_tms, seconds=60))]
)
async def update_note(
        note_id: int,
        note_update: NoteUpdate,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
) -> NoteResponse:
    note_update.tags = ",".join(note_update.tags) if note_update.tags else ""
    note = await dao.update_note(session, note_id, note_update, user)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note.tags = note.tags.split(",") if note.tags != "" else []
    return note


@router.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RateLimiter(times=rl_tms, seconds=60))]
)
async def delete_note(
        note_id: int,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
) -> None:
    await dao.delete_note(session, note_id, user)
