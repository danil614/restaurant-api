from httpx import AsyncClient


async def test_dish_crud(client: AsyncClient):
    # create
    resp = await client.post("/api/v1/dishes/", json={
        "name": "Пицца Маргарита",
        "description": "Классическая пицца",
        "price": 500,
        "category": "Основные блюда"
    })
    assert resp.status_code == 201
    dish_id = resp.json()["id"]

    # list
    resp = await client.get("api/v1/dishes/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # delete
    resp = await client.delete(f"/api/v1/dishes/{dish_id}")
    assert resp.status_code == 204
