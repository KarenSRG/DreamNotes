# app/api/notes.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from datetime import datetime

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/notes/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(
        title=note.title,
        content=note.content,
        tags=','.join(note.tags)  # Преобразуем список тегов в строку
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.get("/notes/", response_model=List[NoteResponse])
def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes


@router.get("/notes/{note_id}", response_model=NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note)
