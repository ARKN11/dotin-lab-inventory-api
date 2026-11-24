from dotin_lab_inventory_api.schemas.product import (
    ProductData,
    ProductCreateData,
    ProductUpdateData,
)
from dotin_lab_inventory_api.repositories import product_repository


def increase_stock(product_id: int, amount: int) -> ProductData | None:
    if amount <= 0:
        raise ValueError("Amount must be a positive integer.")
    product = product_repository.get_by_id(product_id)
    if product is None:
        return None
    return product_repository.update(product_id, {"stock": product["stock"] + amount})


def get_products(
    category: str | None,
    search: str | None,
    skip: int,
    limit: int,
) -> list[ProductData]:
    products = product_repository.get_all()
    if category is not None:
        category = category.lower().strip()
        if not category:
            raise ValueError("Category cannot contain only whitespace")
        products = [
            product for product in products if product["category"].lower() == category
        ]
    if search is not None:
        search = search.lower().strip()
        if not search:
            raise ValueError("Search cannot contain only whitespace")
        products = [
            product for product in products if search in product["name"].lower()
        ]
    return products[skip : skip + limit]


def get_product(product_id: int) -> ProductData | None:
    return product_repository.get_by_id(product_id)


def create_product(product_data: ProductCreateData) -> ProductData:
    return product_repository.create(product_data)


def update_product(
    product_id: int, product_data: ProductUpdateData
) -> ProductData | None:
    return product_repository.update(product_id, product_data)


def delete_product(product_id: int) -> bool:
    return product_repository.delete(product_id)
