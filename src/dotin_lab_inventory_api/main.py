from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    category: str


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None
    category: str | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str


products = {
    1: {
        "id": 1,
        "name": "Laptop",
        "price": 1299.99,
        "stock": 5,
        "category": "Electronics",
    }
}

next_product_id = 2

app = FastAPI(
    title="Dotin Lab Inventory API",
    description="An inventory management REST API.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Dotin Lab Inventory API"}


@app.get("/products", response_model=list[ProductResponse])
def get_products(category: str | None = None):
    if category is not None:
        category = category.lower().strip()
        return [
            product
            for product in products.values()
            if product["category"].lower().strip() == category
        ]
    return list(products.values())


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return products[product_id]


@app.post(
    "/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse
)
def create_product(product: ProductCreate):
    global next_product_id
    product_id = next_product_id
    next_product_id += 1
    products[product_id] = {**product.model_dump(), "id": product_id}
    return products[product_id]


@app.patch("/products/{product_id}")
def partial_update_product(product_id: int, product: ProductUpdate):
    if product_id not in products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    for key, value in product.model_dump(exclude_unset=True).items():
        products[product_id][key] = value

    return products[product_id]


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    del products[product_id]
    return None
