from typing import cast

from fastapi import APIRouter, HTTPException, Query, status

from dotin_lab_inventory_api.schemas.product import (
    ProductCreate,
    ProductCreateData,
    ProductData,
    ProductReplacement,
    ProductResponse,
    ProductUpdate,
    ProductUpdateData,
)
from dotin_lab_inventory_api.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductResponse])
def get_products(
    category: str | None = Query(default=None, min_length=2, max_length=100),
    limit: int = Query(default=10, gt=0, le=100),
    skip: int = Query(default=0, ge=0),
    search: str | None = Query(default=None, min_length=2, max_length=100),
) -> list[ProductData]:
    try:
        products = product_service.get_products(category, search, skip, limit)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        ) from e
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int) -> ProductData:
    product = product_service.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product: ProductCreate) -> ProductData:
    new_product = product_service.create_product(
        cast(ProductCreateData, product.model_dump())
    )
    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductReplacement) -> ProductData:
    new_product = product_service.update_product(
        product_id, cast(ProductUpdateData, product.model_dump())
    )
    if new_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return new_product


@router.patch("/{product_id}", response_model=ProductResponse)
def partial_update_product(product_id: int, product: ProductUpdate) -> ProductData:
    for field in product.model_fields_set:
        if getattr(product, field) is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Field '{field}' cannot be set to None",
            )
    updated_product = product_service.update_product(
        product_id, cast(ProductUpdateData, product.model_dump(exclude_unset=True))
    )
    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int) -> None:
    deleted = product_service.delete_product(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )


@router.post("/{product_id}/increase-stock", response_model=ProductResponse)
def increase_stock(product_id: int, quantity: int = Query(gt=0)) -> ProductData:
    try:
        updated_product = product_service.increase_stock(product_id, quantity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        ) from e
    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return updated_product
