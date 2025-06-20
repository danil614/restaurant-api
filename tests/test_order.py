from httpx import AsyncClient


async def test_order_flow(client: AsyncClient):
    # добавляем блюдо
    resp = await client.post("/api/v1/dishes/", json={
        "name": "Суп",
        "description": "Суп дня",
        "price": 250,
        "category": "Супы"
    })
    dish_id = resp.json()["id"]

    # создаём заказ
    resp = await client.post("/api/v1/orders/", json={
        "customer_name": "Иван",
        "dishes_ids": [dish_id]
    })
    assert resp.status_code == 201
    order = resp.json()
    order_id = order["id"]
    assert order["status"] == "в обработке"

    # меняем статус на 'готовится'
    resp = await client.patch(f"/api/v1/orders/{order_id}/status", json={"status": "готовится"})
    assert resp.json()["status"] == "готовится"

    # попытка пропустить статус -> ошибка
    resp = await client.patch(f"/api/v1/orders/{order_id}/status", json={"status": "завершен"})
    assert resp.status_code == 400
