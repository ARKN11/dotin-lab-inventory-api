from dotin_lab_inventory_api.schemas.product import ProductData, ProductUpdateData, ProductCreateData

products: list[ProductData] = [
    {"id": 10, "name": "Keyboard", "price": 85, "stock": 20, "category": "Electronics"},
    {"id": 25, "name": "Mouse", "price": 25, "stock": 50, "category": "Electronics"},
    {"id": 37, "name": "Monitor", "price": 220, "stock": 15, "category": "Electronics"},
    {"id": 42, "name": "Chair", "price": 150, "stock": 10, "category": "Furniture"},
    {"id": 58, "name": "Desk", "price": 300, "stock": 5, "category": "Furniture"},
    {"id": 63, "name": "Notebook", "price": 5, "stock": 100, "category": "Stationery"},
]

last_product_id: int = max(product["id"] for product in products) if products else 0


def get_next_product_id() -> int:
    global last_product_id
    last_product_id += 1
    return last_product_id


def get_by_id(product_id: int) -> ProductData | None:
    for product in products:
        if product["id"] == product_id:
            target_product = product.copy()
            return target_product
    return None


def create(product_data: ProductCreateData) -> ProductData:
    new_product: ProductData = {
        'id': get_next_product_id(),
        **product_data,
    }
    products.append(new_product)
    return new_product.copy()



def update(product_id: int, product_data: ProductUpdateData) -> ProductData | None:
    for index, product in enumerate(products):
        if product["id"] == product_id:
            updated_product = product.copy()
            updated_product.update(product_data)
            products[index] = updated_product
            return products[index].copy()
    return None


def delete(product_id: int) -> bool:
    for index, product in enumerate(products):
        if product["id"] == product_id:
            del products[index]
            return True
    return False


def get_all() -> list[ProductData]:
    return [product.copy() for product in products]
