from typing import List, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dish import Dish


class DishRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> Sequence[Dish]:
        res = await self.session.scalars(select(Dish))
        return res.all()

    async def create(self, obj_in: dict) -> Dish:
        dish = Dish(**obj_in)
        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    async def delete(self, dish_id: int) -> None:
        await self.session.execute(delete(Dish).where(Dish.id == dish_id))
        await self.session.commit()

    async def get_many(self, ids: List[int]) -> Sequence[Dish]:
        result = await self.session.scalars(select(Dish).where(Dish.id.in_(ids)))
        return result.all()

    async def exists_all(self, ids: List[int]) -> bool:
        dishes = await self.get_many(ids)
        return len(dishes) == len(set(ids))
