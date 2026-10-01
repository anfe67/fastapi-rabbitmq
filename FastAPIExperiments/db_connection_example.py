from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine("postgresql+asyncpg://user:pw@host/db")

@asynccontextmanager
async def get_async_session():
    async with AsyncSession(engine) as session:
        yield session


