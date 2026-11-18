from fastapi import FastAPI, status
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    category: str


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str


app = FastAPI(
    title="Dotin Lab Inventory API",
    description="An inventory management REST API.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Dotin Lab Inventory API"}


@app.get("/products")
def get_products(category: str | None = None):
    return {"category": category}


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    return {
        "id": product_id,
        "name": "laptop",
        "price": 129.99,
        "stock": 5,
        "category": "Electronics",
    }


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    return {"message": "Product created", "product": product}


@app.patch("/products/{product_id}")
def partial_update_product(product_id: int, product: dict):
    return {
        "message": "Product partially updated",
        "product_id": product_id,
        "product": product,
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {"message": "Product deleted", "product_id": product_id}
