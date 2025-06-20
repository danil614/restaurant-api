from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from app.core.config import settings

engine = create_async_engine(settings.sqlalchemy_database_uri, echo=True, future=True, poolclass=NullPool)


@pytest.fixture(scope='session', autouse=True)
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    from app import models
    base_model = models.base.Base

    async with engine.begin() as conn:
        await conn.run_sync(base_model.metadata.drop_all)
        await conn.run_sync(base_model.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(base_model.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def app(db_engine):
    from app.main import app
    from app.core.database import get_session

    async_session_maker = async_sessionmaker(db_engine, expire_on_commit=False)

    async def override_get_db():
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_db
    yield app


@pytest.fixture
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=f"http://test",
                           follow_redirects=True) as client:
        yield client
