from typing import TypedDict

from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: str = Field(min_length=2, max_length=100)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category: str | None = Field(default=None, min_length=2, max_length=100)


class ProductReplacement(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: str = Field(min_length=2, max_length=100)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str


class ProductData(TypedDict):
    id: int
    name: str
    price: float
    stock: int
    category: str


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


app = FastAPI(
    title="Dotin Lab Inventory API",
    description="An inventory management REST API.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Dotin Lab Inventory API"}


@app.get("/products", response_model=list[ProductResponse])
def get_products(
    category: str | None = Query(default=None, min_length=2, max_length=100),
    limit: int = Query(default=10, gt=0, le=100),
    skip: int = Query(default=0, ge=0),
    search: str | None = Query(default=None, min_length=2, max_length=100),
) -> list[ProductData]:
    filtered_products = products
    if category is not None:
        category = category.lower().strip()
        filtered_products = [
            product
            for product in filtered_products
            if product["category"].lower() == category
        ]
    if search is not None:
        search = search.lower().strip()
        filtered_products = [
            product
            for product in filtered_products
            if search in product["name"].lower()
        ]
    return filtered_products[skip : skip + limit]


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int) -> ProductData:
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


@app.post(
    "/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse
)
def create_product(product: ProductCreate) -> ProductData:
    product_id = get_next_product_id()
    new_product: ProductData = {
        "id": product_id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
        "category": product.category,
    }
    products.append(new_product)
    return new_product


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductReplacement) -> ProductData:
    for item in products:
        if item["id"] == product_id:
            item["name"] = product.name
            item["price"] = product.price
            item["stock"] = product.stock
            item["category"] = product.category
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


@app.patch("/products/{product_id}", response_model=ProductResponse)
def partial_update_product(product_id: int, product: ProductUpdate) -> ProductData:
    for item in products:
        if item["id"] == product_id:
            if product.name is not None:
                item["name"] = product.name
            if product.price is not None:
                item["price"] = product.price
            if product.stock is not None:
                item["stock"] = product.stock
            if product.category is not None:
                item["category"] = product.category
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int) -> None:
    for index, product in enumerate(products):
        if product["id"] == product_id:
            del products[index]
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


@app.post("/products/{product_id}/increase-stock", response_model=ProductResponse)
def increase_stock(product_id: int, quantity: int = Query(gt=0)) -> ProductData:
    for product in products:
        if product["id"] == product_id:
            product["stock"] += quantity
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )
