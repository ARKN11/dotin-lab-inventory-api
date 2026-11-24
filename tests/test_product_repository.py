from dotin_lab_inventory_api.repositories import product_repository as repository

import pytest


@pytest.fixture(autouse=True)
def reset_repository():
    repository.products.clear()
    repository.products.extend(
        [
            {
                "id": 10,
                "name": "Keyboard",
                "price": 85,
                "stock": 20,
                "category": "Electronics",
            },
            {
                "id": 25,
                "name": "Mouse",
                "price": 25,
                "stock": 50,
                "category": "Electronics",
            },
            {
                "id": 37,
                "name": "Monitor",
                "price": 220,
                "stock": 15,
                "category": "Electronics",
            },
            {
                "id": 42,
                "name": "Chair",
                "price": 150,
                "stock": 10,
                "category": "Furniture",
            },
            {
                "id": 58,
                "name": "Desk",
                "price": 300,
                "stock": 5,
                "category": "Furniture",
            },
            {
                "id": 63,
                "name": "Notebook",
                "price": 5,
                "stock": 100,
                "category": "Stationery",
            },
        ]
    )
    repository.last_product_id = 63


def test_get_all_returns_all_products():
    products = repository.get_all()

    assert len(products) == 6
    assert products[0]["name"] == "Keyboard"


def test_get_all_returns_independent_data():
    products = repository.get_all()
    products[0]["name"] = "Changed"

    assert repository.get_by_id(10)["name"] == "Keyboard"


def test_get_by_id_returns_product():
    product = repository.get_by_id(25)

    assert product is not None
    assert product["name"] == "Mouse"


def test_get_by_id_returns_none_for_missing_product():
    assert repository.get_by_id(999) is None


def test_get_by_id_returns_independent_data():
    product = repository.get_by_id(10)
    assert product is not None

    product["name"] = "Changed"

    assert repository.get_by_id(10)["name"] == "Keyboard"


def test_create_generates_id_and_stores_product():
    product = repository.create(
        {
            "name": "Headphones",
            "price": 75.0,
            "stock": 12,
            "category": "Electronics",
        }
    )

    assert product["id"] == 64
    assert repository.get_by_id(64) == product


def test_create_returns_independent_data():
    product = repository.create(
        {
            "name": "Webcam",
            "price": 90.0,
            "stock": 8,
            "category": "Electronics",
        }
    )

    product["name"] = "Changed"

    assert repository.get_by_id(product["id"])["name"] == "Webcam"


def test_update_changes_product_without_changing_id():
    updated = repository.update(
        10,
        {"name": "Mechanical Keyboard", "price": 100.0},
    )

    assert updated is not None
    assert updated["id"] == 10
    assert updated["name"] == "Mechanical Keyboard"
    assert updated["price"] == 100.0


def test_update_returns_none_for_missing_product():
    assert repository.update(999, {"name": "Missing"}) is None


def test_update_returns_independent_data():
    updated = repository.update(10, {"name": "Updated Keyboard"})
    assert updated is not None

    updated["name"] = "Changed again"

    assert repository.get_by_id(10)["name"] == "Updated Keyboard"


def test_delete_removes_existing_product():
    assert repository.delete(10) is True
    assert repository.get_by_id(10) is None


def test_delete_returns_false_for_missing_product():
    assert repository.delete(999) is False
