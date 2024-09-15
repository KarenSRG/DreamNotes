from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class NoteBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True


class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
