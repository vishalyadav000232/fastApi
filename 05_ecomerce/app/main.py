from fastapi import FastAPI, status, Query, HTTPException, Path
from app.services.product import get_all_products, delete_product , load_data , create_product_service
from app.schemas.product import Product, ProductResponse , ProductWrapper
from typing import Optional, List
from datetime import datetime
from uuid import uuid4

app = FastAPI(
    title="FastAPI",
    description="This is the FastAPI backend",
    version="2.0.3"
)


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="Successful response 200OK"
)
def root():
    return {
        "message": "Welcome to the FastAPI backend"
    }


@app.get(
    "/products",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse
)
# Path Params With Validation
@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: str = Path(..., example="PROD_007", description="Product id should be in b/w (PROD_001 - PROD_030)")):
    products = get_all_products()
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product id does not math in data base {product_id}"
    )

@app.get("/prod")
def load_product():
    data =load_data()
    return data

# Multiple Path params

@app.get("/products/{product_id}/user/{user_id}", status_code=status.HTTP_200_OK)
def multiple_parameter(product_id: str, user_id: str):
    return {
        "message": f"This is the product id {product_id}, and user id {user_id}"
    }


def load_products(
    name: str = Query(
        None,
        min_length=2,
        max_length=50,
        description="Search the product by the name",
    ),
    sort_by: Optional[str] = Query(
        None,
        description="Sort by: price, rating, stock "
    ),
    sort_order: Optional[str] = Query(
        "asc",
        regex="^(asc|desc)$",
        description="Sort order: asc or desc"
    )
):
    products = get_all_products()

    # Filtering The Products by Name

    if name:
        lower_name = name.strip().lower()
        filtered_products = [p for p in products if lower_name in p.get(
            "name", "").lower()]
        if not filtered_products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Products are not found "
            )
    if sort_by:
        if sort_by not in ["price", "rating", "stock"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort field '{sort_by}'. Choose from: price, rating, stock"
            )
        reverse = True if sort_order == "desc" else False
        products.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
        return {
            "message": "Products fetched successfully",
            "total": len(filtered_products),
            "query": name,
            "products": filtered_products,
            "sorted_products": products
        }

    return {
        "message": "All products fetched successfully",
        "total": len(products),
        "products": products
    }


@app.get("/item/{item_id}", response_model=ProductResponse)
def get_item_with_model(item_id: int):
    """GET endpoint with response model validation"""
    return {
        "id": item_id,
        "name": "Sample Item",
        "price": 9.99,
        "in_stock": True
    }


@app.get("/old-endpoint", deprecated=True)
def old_endpoint():
    """GET endpoint marked as deprecated"""
    return {"message": "This endpoint is deprecated"}


@app.get("/logs")
def get_logs(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...)
):
    """GET with datetime query parameters"""
    return {"start": start_date, "end": end_date}


@app.get("/tags")
def get_tags(tags: List[str] = Query(...)):
    """
    Accept multiple tags as query parameters
    Usage: /tags?tags=python&tags=fastapi&tags=web
    Returns: {"tags": ["python", "fastapi", "web"]}
    """
    return {"tags": tags}



@app.post(
    "/create_product",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductWrapper
)
def add_product(product: Product):

    try:
        new_product = create_product_service(product.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    return {
        "message": "Product added successfully",
        "products": new_product,  
    }


# Deleted Products

@app.delete("/products/{product_id}", status_code=status.HTTP_200_OK , response_model=ProductWrapper)
def remove_products(product_id:str = Path(... , example="PROD_031")):
    try:
        deleted_product = delete_product(product_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    return {
        "message": "Product Deleted successfully",
        "products": deleted_product,  
    }
