import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def test_create_and_list_item():
    warehouse = client.post("/warehouses", json={"name": unique("wh")})
    assert warehouse.status_code == 201

    sku = unique("sku")
    item = client.post("/items", json={"sku": sku, "quantity": 5, "warehouse_id": warehouse.json()["id"]})
    assert item.status_code == 201

    skus = [row["sku"] for row in client.get("/items").json()]
    assert sku in skus


def test_duplicate_sku_is_rejected():
    warehouse_id = client.post("/warehouses", json={"name": unique("wh")}).json()["id"]
    sku = unique("sku")
    first = client.post("/items", json={"sku": sku, "warehouse_id": warehouse_id})
    second = client.post("/items", json={"sku": sku, "warehouse_id": warehouse_id})
    assert (first.status_code, second.status_code) == (201, 409)


def test_item_needs_an_existing_warehouse():
    response = client.post("/items", json={"sku": unique("sku"), "warehouse_id": 999999})
    assert response.status_code == 404
