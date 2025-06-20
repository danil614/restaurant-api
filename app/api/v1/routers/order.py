from typing import List, Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.services import get_order_service
from app.api.v1.services.order import OrderService
from app.schemas.order import OrderRead, OrderCreate, OrderUpdateStatus

router = APIRouter(prefix="/orders", tags=["Orders"])
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]


@router.get("/", response_model=List[OrderRead])
async def list_orders(service: OrderServiceDep):
    return await service.list()


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(data: OrderCreate, service: OrderServiceDep):
    return await service.create(data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(order_id: int, service: OrderServiceDep):
    await service.cancel(order_id)


@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_status(order_id: int,
                        data: OrderUpdateStatus,
                        service: OrderServiceDep):
    return await service.update_status(order_id, data)
