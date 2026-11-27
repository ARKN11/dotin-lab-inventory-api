import logging

from fastapi import FastAPI

from dotin_lab_inventory_api.routers.products import router as products_router
from dotin_lab_inventory_api.middleware.observability import (
    observability_middleware,
)

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Dotin Lab Inventory API",
    description="An inventory management REST API.",
    version="0.1.0",
)

app.middleware("http")(observability_middleware)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {"message": "Dotin Lab Inventory API"}


app.include_router(products_router)
