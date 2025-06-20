from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.dish import DishRepository
from app.repositories.order import OrderRepository


async def get_dish_repository(
        session: Annotated[AsyncSession, Depends(get_session)]
) -> AsyncGenerator[DishRepository, None]:
    yield DishRepository(session)


async def get_order_repository(
        session: Annotated[AsyncSession, Depends(get_session)]
) -> AsyncGenerator[OrderRepository, None]:
    yield OrderRepository(session)
