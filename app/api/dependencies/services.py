from typing import AsyncGenerator, Annotated

from fastapi import Depends

from app.api.dependencies.repositories import get_dish_repository, get_order_repository
from app.api.v1.services.dish import DishService
from app.api.v1.services.order import OrderService
from app.repositories.dish import DishRepository
from app.repositories.order import OrderRepository


async def get_dish_service(
        dish_repo: Annotated[DishRepository, Depends(get_dish_repository)]
) -> AsyncGenerator[DishService, None]:
    yield DishService(dish_repo)


async def get_order_service(
        order_repo: Annotated[OrderRepository, Depends(get_order_repository)],
        dish_repo: Annotated[DishRepository, Depends(get_dish_repository)]
) -> AsyncGenerator[OrderService, None]:
    yield OrderService(order_repo, dish_repo)
