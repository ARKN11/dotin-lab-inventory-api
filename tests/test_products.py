from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from dotin_lab_inventory_api import main

INITIAL_PRODUCTS = [
    {"id": 10, "name": "Keyboard", "price": 85, "stock": 20, "category": "Electronics"},
    {"id": 25, "name": "Mouse", "price": 25, "stock": 50, "category": "Electronics"},
    {"id": 37, "name": "Monitor", "price": 220, "stock": 15, "category": "Electronics"},
    {"id": 42, "name": "Chair", "price": 150, "stock": 10, "category": "Furniture"},
    {"id": 58, "name": "Desk", "price": 300, "stock": 5, "category": "Furniture"},
    {"id": 63, "name": "Notebook", "price": 5, "stock": 100, "category": "Stationery"},
]


@pytest.fixture
def client(monkeypatch):
    # Give every test an independent copy of the initial in-memory data.
    monkeypatch.setattr(main, "products", deepcopy(INITIAL_PRODUCTS))
    monkeypatch.setattr(main, "last_product_id", 63)
    return TestClient(main.app)


def test_root_returns_api_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Dotin Lab Inventory API"}


def test_get_products_returns_all_products(client):
    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 6


def test_get_products_filters_by_category_case_insensitively(client):
    response = client.get("/products", params={"category": "electronics"})

    assert response.status_code == 200
    assert [product["id"] for product in response.json()] == [10, 25, 37]


def test_get_products_searches_by_name(client):
    response = client.get("/products", params={"search": "key"})

    assert response.status_code == 200
    assert [product["id"] for product in response.json()] == [10]


def test_get_products_applies_pagination(client):
    response = client.get("/products", params={"skip": 1, "limit": 2})

    assert response.status_code == 200
    assert [product["id"] for product in response.json()] == [25, 37]


def test_get_products_combines_filters_and_pagination(client):
    response = client.get(
        "/products",
        params={"category": "electronics", "search": "mo", "skip": 1, "limit": 1},
    )

    assert response.status_code == 200
    assert [product["id"] for product in response.json()] == [37]


@pytest.mark.parametrize(
    ("params", "expected_status"),
    [
        ({"limit": 0}, 422),
        ({"limit": 101}, 422),
        ({"skip": -1}, 422),
        ({"search": "x"}, 422),
    ],
)
def test_get_products_rejects_invalid_query_parameters(client, params, expected_status):
    response = client.get("/products", params=params)

    assert response.status_code == expected_status


def test_get_product_returns_matching_product(client):
    response = client.get("/products/25")

    assert response.status_code == 200
    assert response.json()["name"] == "Mouse"


def test_get_product_returns_404_for_unknown_id(client):
    response = client.get("/products/999")

    assert response.status_code == 404


def test_create_product_returns_201_and_generates_id(client):
    payload = {
        "name": "Webcam",
        "price": 75,
        "stock": 12,
        "category": "Electronics",
    }

    response = client.post("/products", json=payload)

    assert response.status_code == 201
    assert response.json() == {"id": 64, **payload}


def test_create_product_rejects_invalid_data(client):
    payload = {
        "name": "Webcam",
        "price": 0,
        "stock": 12,
        "category": "Electronics",
    }

    response = client.post("/products", json=payload)

    assert response.status_code == 422


def test_put_replaces_product_fields_and_preserves_id(client):
    payload = {
        "name": "Wireless Mouse",
        "price": 40,
        "stock": 30,
        "category": "Accessories",
    }

    response = client.put("/products/25", json=payload)

    assert response.status_code == 200
    assert response.json() == {"id": 25, **payload}


def test_put_returns_404_for_unknown_product(client):
    payload = {
        "name": "Wireless Mouse",
        "price": 40,
        "stock": 30,
        "category": "Accessories",
    }

    response = client.put("/products/999", json=payload)

    assert response.status_code == 404


def test_patch_updates_only_supplied_fields(client):
    response = client.patch("/products/25", json={"price": 35})

    assert response.status_code == 200
    assert response.json()["price"] == 35
    assert response.json()["name"] == "Mouse"
    assert response.json()["stock"] == 50


def test_patch_rejects_explicit_null_values(client):
    response = client.patch("/products/25", json={"name": None, "price": 35})

    assert response.status_code == 422
    assert response.json()["detail"] == "Field 'name' cannot be set to None"

    unchanged_product = client.get("/products/25")
    assert unchanged_product.status_code == 200
    assert unchanged_product.json() == {
        "id": 25,
        "name": "Mouse",
        "price": 25,
        "stock": 50,
        "category": "Electronics",
    }


def test_patch_rejects_invalid_values(client):
    response = client.patch("/products/25", json={"price": -1})

    assert response.status_code == 422


def test_patch_returns_404_for_unknown_product(client):
    response = client.patch("/products/999", json={"price": 35})

    assert response.status_code == 404


def test_delete_returns_204_with_empty_body(client):
    response = client.delete("/products/25")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/products/25").status_code == 404


def test_delete_returns_404_for_unknown_product(client):
    response = client.delete("/products/999")

    assert response.status_code == 404


def test_increase_stock_updates_and_returns_product(client):
    response = client.post("/products/25/increase-stock", params={"quantity": 10})

    assert response.status_code == 200
    assert response.json()["stock"] == 60


@pytest.mark.parametrize("quantity", [0, -5])
def test_increase_stock_rejects_non_positive_quantity(client, quantity):
    response = client.post("/products/25/increase-stock", params={"quantity": quantity})

    assert response.status_code == 422


def test_increase_stock_requires_quantity(client):
    response = client.post("/products/25/increase-stock")

    assert response.status_code == 422


def test_increase_stock_returns_404_for_unknown_product(client):
    response = client.post("/products/999/increase-stock", params={"quantity": 10})

    assert response.status_code == 404


@pytest.mark.parametrize(
    "field",
    ["name", "category"],
)
def test_create_product_rejects_whitespace_only_text(client, field):
    payload = {
        "name": "Webcam",
        "price": 75,
        "stock": 12,
        "category": "Electronics",
    }
    payload[field] = "   "

    response = client.post("/products", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field",
    ["name", "category"],
)
def test_put_rejects_whitespace_only_text(client, field):
    payload = {
        "name": "Wireless Mouse",
        "price": 40,
        "stock": 30,
        "category": "Accessories",
    }
    payload[field] = "   "

    response = client.put("/products/25", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field",
    ["name", "category"],
)
def test_patch_rejects_whitespace_only_text_without_modifying_product(client, field):
    original_product = client.get("/products/25").json()

    response = client.patch(
        "/products/25",
        json={field: "   "},
    )

    assert response.status_code == 422

    unchanged_product = client.get("/products/25").json()
    assert unchanged_product == original_product


def test_patch_rejects_empty_body(client):
    response = client.patch("/products/25", json={})

    assert response.status_code == 422

    unchanged_product = client.get("/products/25").json()
    assert unchanged_product["name"] == "Mouse"
    assert unchanged_product["price"] == 25
