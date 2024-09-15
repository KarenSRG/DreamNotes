from sqlalchemy import Integer, String, TIMESTAMP, func
from sqlalchemy.orm import mapped_column, relationship
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String, unique=True)
    hashed_password = mapped_column(String)
    created_at = mapped_column(TIMESTAMP, server_default=func.now())

    notes = relationship("Note", back_populates="owner")
