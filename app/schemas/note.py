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
    pass


class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
