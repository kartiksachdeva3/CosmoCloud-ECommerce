from bson import ObjectId
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int

class ProductUpdate(BaseModel):
    name: str
    price: float
    quantity: int
class PaginatedProduct(BaseModel):
    data: list[Product]
    page: dict

