from typing import Annotated, TypedDict, Self

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)

ProductName = Annotated[str, Field(min_length=2, max_length=100)]
ProductPrice = Annotated[float, Field(gt=0)]
ProductStock = Annotated[int, Field(ge=0)]
ProductCategory = Annotated[str, Field(min_length=2, max_length=100)]


def validate_text(value: str) -> str:
    if not value.strip():
        raise ValueError("Value cannot contain only whitespace")

    return value


class ProductBase(BaseModel):
    name: ProductName
    price: ProductPrice
    stock: ProductStock
    category: ProductCategory

    @field_validator("name", "category", mode="after")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        return validate_text(value)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: ProductName | None = None
    price: ProductPrice | None = None
    stock: ProductStock | None = None
    category: ProductCategory | None = None

    @field_validator("name", "category", mode="after")
    @classmethod
    def validate_text_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_text(value)

    @model_validator(mode="after")
    def validate_update(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        return self


class ProductReplacement(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int


class ProductData(TypedDict):
    id: int
    name: str
    price: float
    stock: int
    category: str


class ProductCreateData(TypedDict):
    name: str
    price: float
    stock: int
    category: str


class ProductUpdateData(TypedDict, total=False):
    name: str
    price: float
    stock: int
    category: str
