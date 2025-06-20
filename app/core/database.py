from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.sqlalchemy_database_uri,
    echo=False,
)

async_session_factory = async_sessionmaker(
    engine, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:  # dependency для FastAPI
    async with async_session_factory() as session:
        yield session
