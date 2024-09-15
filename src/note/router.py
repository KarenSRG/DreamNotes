import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.note.schema import NoteCreate, NoteUpdate, NoteResponse

from src.note.dao import create_note, get_note_by_id, get_notes_by_owner
from src.note.dao import update_note, delete_note

from src.user.auth import get_current_user

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/notes/", response_model=NoteResponse)
def create_new_note(note: NoteCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        db_note = create_note(db, note, user.id)
        return db_note
    except HTTPException as e:
        logger.error(f"Failed to create note: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/notes/", response_model=List[NoteResponse])
def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        notes = get_notes_by_owner(db, user.id, skip, limit)
        return notes
    except HTTPException as e:
        logger.error(f"Failed to retrieve notes: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/notes/{note_id}", response_model=NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        note = get_note_by_id(db, note_id, user.id)
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
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db),
                user: int = Depends(get_current_user)):
    try:
        note = update_note(db, note_id, note_update, user.id)
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
def delete_note(note_id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        delete_note(db, note_id, user.id)
    except HTTPException as e:
        logger.error(f"Failed to delete note: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
