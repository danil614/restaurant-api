from fastapi import FastAPI

from app.api.v1.routers import dish, order
from app.core.config import settings

app = FastAPI(title=settings.api_title, version=settings.api_version)

app.include_router(dish.router, prefix='/api/v1')
app.include_router(order.router, prefix='/api/v1')
