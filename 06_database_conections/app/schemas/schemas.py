# schemas.py
from pydantic import BaseModel

# Base class for products
class ProductBase(BaseModel):
    name: str
    price: float

# Schema for creating a product
class ProductCreate(ProductBase):
    pass

# Schema for reading a product (includes ID)
class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True  # <-- correct
