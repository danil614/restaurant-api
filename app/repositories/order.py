from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> Sequence[Order]:
        res = await self.session.scalars(select(Order).options(selectinload(Order.dishes)))
        return res.all()

    async def create(self, order: Order) -> Order:
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get(self, order_id: int) -> Order | None:
        res = await self.session.scalars(
            select(Order).where(Order.id == order_id).options(selectinload(Order.dishes))
        )
        return res.first()

    async def delete(self, order_id: int):
        await self.session.execute(delete(Order).where(Order.id == order_id))
        await self.session.commit()

    async def save(self, order: Order):
        await self.session.commit()
        await self.session.refresh(order)
