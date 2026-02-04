from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Dict, Any, List, Optional


class Metadata(BaseModel):
    version: str
    lastUpdated: str
    totalProducts: int
    currency: str


class Product(BaseModel):
    id: str = Field(..., example="PROD_007")
    sku: str = Field(..., example="SKU-ELECTRO-001")
    name: str = Field(..., example="Industrial Variable Frequency Drive")
    category: str = Field(..., example="Electronics/Power")
    subcategory: str = Field(..., example="Power Electronics")
    description: str = Field(...,
                             example="3-phase industrial VFD for motor speed control")
    price: float = Field(..., example=8900.00)
    costPrice: float = Field(..., example=5200.00)
    discount: float = Field(..., example=6)
    stock: int = Field(..., example=78)
    manufacturer: str = Field(..., example="PowerTech Motors")
    specifications: Dict[str, Any] = Field(..., example={
        "capacity": "75kW",
        "inputVoltage": "380-480V",
        "efficiency": "98.5%",
        "coolingType": "Forced Air"
    })
    rating: Optional[float] = Field(default=0.0, example=4.6)
    reviews: Optional[int] = Field(default=0, example=423)

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value: str):
        if not value or not value.strip():
            raise ValueError("SKU cannot be empty")
        return value
    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price - (self.price * self.discount / 100), 2)

class ProductResponse(BaseModel):
    message: str
    metadata: Metadata
    total: int
    query: Optional[str] = None
    products: List[Product]
    sorted_products: Optional[List[Product]] = None


class ProductWrapper(BaseModel):
    message: str
    products: Dict[str , Any]
