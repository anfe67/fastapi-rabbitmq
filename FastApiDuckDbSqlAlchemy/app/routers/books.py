# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from ..models import Book

router = APIRouter(prefix="/books", tags=["books"])


# ---------- Pydantic shapes ----------------------------------------------
class BookIn(BaseModel):
    title: str
    year: int | None = None
    genre: str = "unknown"


class BookOut(BaseModel):
    id: int
    title: str
    year: int | None
    genre: str
    model_config = {"from_attributes": True}


# ---------- Session dependency ------------------------------------------
def get_db(request: Request):
    session = request.app.state.db()
    try:
        yield session
    finally:
        session.close()


# ---------- CRUD --------------------------------------------------------
@router.get("", response_model=list[BookOut])
def list_books(
    genre: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    stmt = select(Book)
    if genre:
        stmt = stmt.where(Book.genre == genre)
    stmt = stmt.order_by(Book.id).offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.get("/summary")
def genre_summary(request: Request):
    with request.app.state.db() as db:
        res = db.execute(text("""
            SELECT b.genre,
                   COUNT(*)            AS n_books,
                   MIN(b.year)         AS earliest,
                   MAX(b.year)         AS latest,
                   COALESCE(SUM(s.amount),0) AS revenue
            FROM books b
            LEFT JOIN sales s ON s.book_id = b.id
            GROUP BY b.genre
            ORDER BY revenue DESC
        """))
        cols = [c[0] for c in res.cursor.description]
        return [dict(zip(cols, row)) for row in res.fetchall()]


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(404, "Book not found")
    return book


@router.post("", response_model=BookOut, status_code=201)
def create_book(book: BookIn, db: Session = Depends(get_db)):
    # Get next ID manually since DuckDB doesn't support autoincrement
    result = db.execute(text("SELECT COALESCE(MAX(id), 0) + 1 FROM books"))
    next_id = result.scalar()
    new = Book(id=next_id, **book.model_dump())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(404, "Book not found")
    db.delete(book)
    db.commit()


@router.get("/sales/parquet")
def sales_from_parquet(request: Request, year: int | None = None):
    sql = "SELECT region, SUM(amount) AS total FROM read_parquet('data/sales/*.parquet')"
    params = {}
    if year is not None:
        sql += " WHERE year = :year"
        params["year"] = year
    sql += " GROUP BY region ORDER BY total DESC"
    with request.app.state.db() as db:
        res = db.execute(text(sql), params)
        cols = [c[0] for c in res.cursor.description]
        return [dict(zip(cols, row)) for row in res.fetchall()]