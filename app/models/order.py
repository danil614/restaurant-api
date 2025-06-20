import enum
from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, Enum, DateTime, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now
from app.models.dish import Dish

order_dish = Table(
    "order_dish",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
    Column("dish_id", ForeignKey("dishes.id", ondelete="CASCADE"), primary_key=True),
)


class OrderStatus(str, enum.Enum):
    PROCESSING = "в обработке"
    COOKING = "готовится"
    DELIVERING = "доставляется"
    COMPLETED = "завершен"


class Order(Base):
    __tablename__ = "orders"

    customer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    order_time: Mapped[datetime] = mapped_column(DateTime(True), default=utc_now)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PROCESSING)

    dishes: Mapped[List[Dish]] = relationship(
        secondary=order_dish,
        cascade="all, delete",
        lazy="selectin",
    )
