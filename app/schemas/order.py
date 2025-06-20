from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models.order import OrderStatus
from app.schemas.dish import DishRead


class OrderCreate(BaseModel):
    customer_name: str = Field(..., max_length=120)
    dishes_ids: List[int] = Field(..., min_length=1)


class OrderRead(BaseModel):
    id: int
    customer_name: str
    order_time: datetime
    status: OrderStatus
    dishes: List[DishRead]

    class Config:
        from_attributes = True


class OrderUpdateStatus(BaseModel):
    status: OrderStatus
