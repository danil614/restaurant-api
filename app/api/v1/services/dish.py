from app.repositories.dish import DishRepository
from app.schemas.dish import DishCreate


class DishService:
    def __init__(self, repo: DishRepository):
        self.repo = repo

    async def create(self, schema: DishCreate):
        return await self.repo.create(schema.model_dump())

    async def delete(self, dish_id: int):
        await self.repo.delete(dish_id)

    async def list(self):
        return await self.repo.list()
