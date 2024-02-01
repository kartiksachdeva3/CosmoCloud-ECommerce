from fastapi import APIRouter, HTTPException, Query
from app.models.product  import Product, ProductCreate, ProductUpdate, PaginatedProduct
from typing import List
from pymongo import MongoClient
from bson import ObjectId

router = APIRouter()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Cloud"]
products_collection = db["products"]

@router.get("/all", response_model=List[Product])
async def get_all_product():
    product = list(products_collection.find())
    
    return product

@router.get("/", response_model=PaginatedProduct)
async def get_products(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_price: float = Query(None),
    max_price: float = Query(None),
):
    # Match stage for filters
    match_stage = {
        "price": {"$gte": min_price} if min_price is not None else {"$exists": True},
        "price": {"$lte": max_price} if max_price is not None else {"$exists": True},
    }

    # Pipeline stages for pagination and filtering
    pipeline = [
        {"$match": match_stage},
        {"$facet": {
            "data": [
                {"$skip": offset},
                {"$limit": limit},
            ],
            "page": [
                {"$count": "total"},
            ],
        }},
    ]

    # Execute the aggregation pipeline
    result = list(products_collection.aggregate(pipeline))

    # Extract data and page facets
    data = result[0]["data"]
    page_facet = result[0]["page"][0] if result and "page" in result[0] else {}

    # Calculate next and previous offsets
    next_offset = offset + limit if offset + limit < page_facet.get("total", 0) else None
    prev_offset = offset - limit if offset - limit >= 0 else None

    # Create paginated response
    paginated_response = {
        "data": data,
        "page": {
            "limit": limit,
            "nextOffset": next_offset,
            "prevOffset": prev_offset,
            **page_facet,
        },
    }

    return paginated_response

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate):
    product_data = dict(product)
    result = products_collection.insert_one(product_data)
    product_data["_id"] = str(result.inserted_id)

    return product_data


@router.get("/{product_id}", response_model=dict)
async def read_product(product_id: str):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=dict)
async def update_product(product_id: str, product: ProductUpdate):
    product_data = dict(product)
    result = products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data["_id"] = str(result.inserted_id)
    return product_data

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    result = products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}