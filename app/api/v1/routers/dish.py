from typing import List, Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.services import get_dish_service
from app.api.v1.services.dish import DishService
from app.schemas.dish import DishRead, DishCreate

router = APIRouter(prefix="/dishes", tags=["Dishes"])
DishServiceDep = Annotated[DishService, Depends(get_dish_service)]


@router.get("/", response_model=List[DishRead])
async def list_dishes(service: DishServiceDep):
    return await service.list()


@router.post("/", response_model=DishRead, status_code=status.HTTP_201_CREATED)
async def add_dish(data: DishCreate, service: DishServiceDep):
    return await service.create(data)


@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(dish_id: int, service: DishServiceDep):
    await service.delete(dish_id)
