from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"


class Thread(Base):
    __tablename__ = "threads"

    id: Mapped[int] = mapped_column(primary_key=True)

    ## TODO: add user if needed
    textmessage = relationship("TextMessage", back_populates="thread")
    ##created_timestamp: Mapped[datetime] = mapped_column(default=datetime.now)


class TextMessage(Base):

    __tablename__ = "textmessages"

    id: Mapped[int] = mapped_column(primary_key=True)

    thread_id : Mapped[int] = mapped_column(ForeignKey("threads.id"))
    thread = relationship("Thread", back_populates="textmessage")
    content: Mapped[str]
    is_request: Mapped[bool]
    created_timestamp: Mapped[datetime] = mapped_column(default=datetime.now) 