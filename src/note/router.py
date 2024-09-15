import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.note.schema import NoteCreate, NoteUpdate, NoteResponse
from src.note import dao
from src.user.auth import get_current_user
from src.user.model import User

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/notes/", response_model=NoteResponse)
async def create_note(
        note: NoteCreate,
        user: User = Depends(get_current_user)
) -> NoteResponse:
    try:
        db_note = await dao.create_note(note, user)
        return db_note
    except HTTPException as e:
        logger.error(f"Failed to create note: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/notes/", response_model=List[NoteResponse])
async def read_notes(
        skip: int = 0,
        limit: int = 10,
        user: User = Depends(get_current_user)
) -> List[NoteResponse]:
    try:
        notes = await dao.get_notes_by_owner(user.id, skip, limit)
        return notes
    except HTTPException as e:
        logger.error(f"Failed to retrieve notes: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/notes/{note_id}", response_model=NoteResponse)
async def read_note(
        note_id: int,
        user: User = Depends(get_current_user)
) -> NoteResponse:
    try:
        note = await dao.get_note_by_id(note_id, user.id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    except HTTPException as e:
        logger.error(f"Failed to retrieve note: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(
        note_id: int,
        note_update: NoteUpdate,
        user: User = Depends(get_current_user)
) -> NoteResponse:
    try:
        note = await dao.update_note(note_id, note_update, user)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    except HTTPException as e:
        logger.error(f"Failed to update note: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
        note_id: int,
        user: User = Depends(get_current_user)
) -> None:
    try:
        await dao.delete_note(note_id, user.id)
    except HTTPException as e:
        logger.error(f"Failed to delete note: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
