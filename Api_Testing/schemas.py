from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import ClassVar

class Specification(BaseModel):
    # This is just a normal variable, it will not be part of the schema validation
    VALID_COLORS: ClassVar[list[str]] = ["red", "green", "blue", "yellow", "black", "white", "pink", "orange", "purple", "gray"]
    
    color: str = Field(min_length=1, max_length=30)
    weight: float = Field(gt=0)  # Weight in kilograms
    height: float = Field(gt=0)  # Height in centimeters
    length: float = Field(gt=0)  # Length in centimeters

    @field_validator('color')
    def validate_color(cls, value):
        """
        Checks that the added color is valid
        """
        if value.lower() not in cls.VALID_COLORS:
            raise ValueError(f"Invalid color. Allowed colors are: {', '.join(cls.VALID_COLORS)}")
        return value

class ProductSchema(BaseModel):
    # This is just a normal variable, it will not be part of the schema validation
    VALID_CATEGORIES: ClassVar[list[str]] = ["Electronics", "Clothing", "Home & Garden", "Toys & Games", "Beauty & Health"]

    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, lt=1000000)
    category: str = Field(min_length=3, max_length=30)
    specification: Specification
    description: str | None = Field(default=None, max_length=200)
    stock: int = Field(ge=0)

    @field_validator('category')
    def validate_category(cls, value):
        """
        Checks that the category is valid
        """
        if value not in cls.VALID_CATEGORIES:
            raise ValueError(f"Invalid category. Allowed categories are: {', '.join(cls.VALID_CATEGORIES)}")
        return value

class BulkProductSchema(BaseModel):
    products: list[ProductSchema] = Field(embed=True)
    # Other fields and validators as previously mentioned