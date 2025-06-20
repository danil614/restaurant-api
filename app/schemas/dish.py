from typing import Optional

from pydantic import BaseModel, Field


class DishCreate(BaseModel):
    name: str = Field(..., max_length=120)
    description: Optional[str] = Field(default=None, max_length=255)
    price: float = Field(..., ge=0)
    category: Optional[str] = Field(default=None, max_length=80)


class DishRead(DishCreate):
    id: int

    class Config:
        from_attributes = True
