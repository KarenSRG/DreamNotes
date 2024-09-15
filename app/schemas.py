from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Схемы для пользователя
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str  # Поле для создания пользователя, т.к. хэшированный пароль хранится в базе


class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # Вместо orm_mode в Pydantic 2


# Схемы для заметок
class NoteBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []  # Теги как список строк


class NoteCreate(NoteBase):
    pass  # Для создания заметки достаточно базовых полей


class Note(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int  # Владелец заметки

    class Config:
        from_attributes = True

    # Схема для аутентификации (токены)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
