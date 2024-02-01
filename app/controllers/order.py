from fastapi import APIRouter, HTTPException
from app.models.order import OrderCreate, OrderItem, UserAddress
from app.controllers.product import ProductUpdate
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Cloud"]
orders_collection = db["orders"]

products_collection = db["products"] 


@router.post("/", response_model=dict)
async def create_order(order_create: OrderCreate):
   
    # Calculate total amount for each order item

    product = products_collection.find_one({"_id": ObjectId(order_create.items.productId)})
    if order_create.items.boughtQuantity > product["quantity"]:
            raise HTTPException(status_code=400, detail=f"Insufficient quantity available for product {product['name']}")
        
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {order_create.items.productId} not found")
    order_create.items.totalAmount = order_create.items.boughtQuantity * product["price"]

    # Calculate total amount for the entire order
    

    # Create the order document
    order_data = {
        "createdOn": datetime.utcnow(),
        "items": dict(order_create.items),
        "UserAddress": dict(order_create.userAddress),
        "total_order_amount" : order_create.items.totalAmount,
    }
    product_refresh = {
         "name" : product['name'],
         "price": product['price'],
         "quantity": product['quantity'] - order_create.items.boughtQuantity
    }
    if order_data:
         result_update = products_collection.update_one({"_id": ObjectId(order_create.items.productId)}, {"$set": product_refresh})
        #  print(result_update)
    result = orders_collection.insert_one(order_data)
    
   
    order_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
    return order_data