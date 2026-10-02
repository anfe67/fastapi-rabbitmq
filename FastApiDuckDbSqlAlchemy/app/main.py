# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import SessionLocal, init_db
from .routers import books


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()                      # creates tables in app.duckdb
    app.state.db = SessionLocal    # expose session factory to endpoints
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(books.router)
    return app