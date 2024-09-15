from sqlalchemy import Integer, String, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import mapped_column, relationship
from src.database import Base


class Note(Base):
    __tablename__ = "notes"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, index=True)
    content = mapped_column(Text)
    tags = mapped_column(String)
    created_at = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    owner_id = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="notes")
