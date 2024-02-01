from typing import List
from pydantic import BaseModel

class OrderItem(BaseModel):
    productId: str
    boughtQuantity: int
    totalAmount: float

class UserAddress(BaseModel):
    city: str
    country: str
    zipCode: str

class OrderCreate(BaseModel):
    items: OrderItem
    userAddress: UserAddress
    
