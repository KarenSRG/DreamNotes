from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), unique=True, index=True)
    email = mapped_column(String(100), unique=True, index=True)
    hashed_password = mapped_column(String(100))  # Сохраняем хэшированный пароль

    notes = relationship('Note', back_populates='owner')


class Note(Base):
    __tablename__ = 'notes'

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(100))
    content = mapped_column(Text)
    tags = mapped_column(
        String(200))  # Сохранение тегов как строка. Можете использовать другой способ хранения, например, JSON
    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = mapped_column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='notes')
