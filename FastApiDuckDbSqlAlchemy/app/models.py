# app/models.py
from datetime import datetime

from sqlalchemy import (
    DateTime, ForeignKey, Integer, String, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base, engine


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int | None]
    genre: Mapped[str] = mapped_column(String, default="unknown")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    sales: Mapped[list["Sale"]] = relationship(back_populates="book")


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    amount: Mapped[float]
    sold_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    book: Mapped["Book"] = relationship(back_populates="sales")


def init_db() -> None:
    Base.metadata.create_all(engine)


def drop_db() -> None:
    Base.metadata.drop_all(engine)