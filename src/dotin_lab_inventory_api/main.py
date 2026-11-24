from fastapi import FastAPI

from dotin_lab_inventory_api.routers.products import router as products_router

app = FastAPI(
    title="Dotin Lab Inventory API",
    description="An inventory management REST API.",
    version="0.1.0",
)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {"message": "Dotin Lab Inventory API"}


app.include_router(products_router)
