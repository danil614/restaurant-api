from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Dish(Base):
    __tablename__ = "dishes"

    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(80))
