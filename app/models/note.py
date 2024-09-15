from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from app.database import Base
from datetime import datetime


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    tags: Mapped[str] = mapped_column(String(200))  # Сохраняем теги как строку
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.now())
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='notes')
