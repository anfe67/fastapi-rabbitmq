# app/db.py
from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# Import dialect registration first (separate module to avoid circular import)
import app.dialect  # noqa: F401 - registers the duckdb dialect

# --- Engine, Session, metadata -------------------------------------------
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Use absolute path for database file to ensure persistence
db_path = Path(__file__).parent.parent / "app.duckdb"
engine = create_engine(
    f"duckdb:///{db_path}",      # file-backed; use "" for :memory:
    pool_size=5,                 # one connection pool, like any other DB
    max_overflow=10,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)