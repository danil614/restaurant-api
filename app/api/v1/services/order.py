from fastapi import HTTPException, status

from app.models.order import Order, OrderStatus
from app.repositories.dish import DishRepository
from app.repositories.order import OrderRepository
from app.schemas.order import OrderCreate, OrderUpdateStatus

STATUS_FLOW = [
    OrderStatus.PROCESSING,
    OrderStatus.COOKING,
    OrderStatus.DELIVERING,
    OrderStatus.COMPLETED,
]
STATUS_INDEX = {v: i for i, v in enumerate(STATUS_FLOW)}


class OrderService:
    def __init__(self, order_repo: OrderRepository, dish_repo: DishRepository):
        self.order_repo = order_repo
        self.dish_repo = dish_repo

    async def list(self):
        return await self.order_repo.list()

    async def create(self, schema: OrderCreate):
        # проверяем существование всех блюд
        if not await self.dish_repo.exists_all(schema.dishes_ids):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="One or more dishes not found")

        dishes = await self.dish_repo.get_many(schema.dishes_ids)
        order = Order(customer_name=schema.customer_name, dishes=list(dishes))
        return await self.order_repo.create(order)

    async def cancel(self, order_id: int):
        order = await self.order_repo.get(order_id)
        if not order:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")
        if order.status != OrderStatus.PROCESSING:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="Only orders in 'processing' status can be canceled")
        await self.order_repo.delete(order_id)

    async def update_status(self, order_id: int, data: OrderUpdateStatus):
        order = await self.order_repo.get(order_id)
        if not order:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")

        current_i = STATUS_INDEX[order.status]
        target_i = STATUS_INDEX[data.status]

        if target_i - current_i != 1:  # разрешён только следующий этап
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="Status change must be sequential")

        order.status = data.status
        await self.order_repo.save(order)
        return order
