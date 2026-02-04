import json
from pathlib import Path
from typing import Dict, Any
from datetime import date
from fastapi import HTTPException , status

DATA_FILE = Path(__file__).parent.parent / "data" / "product.json"


def load_data() -> Dict[str, Any]:
    if not DATA_FILE.exists():
        return {
            "metadata": {
                "version": "1.0",
                "lastUpdated": "",
                "totalProducts": 0,
                "currency": "USD"
            },
            "products": []
        }
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        raise RuntimeError("Invalid JSON format in dummy.json")


def get_all_products():
    data = load_data()
    return data["products"]


def save_data(data: Dict[str, Any]) -> None:
   
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )
    except Exception as e:
        raise RuntimeError(f"Failed to save data: {e}")

# ADD PRODUCTS / CREATE

def create_product_service(product: Dict[str, Any]) -> Dict[str, Any]:
    data = load_data()

    # Duplicate check
    for p in data["products"]:
        if p["id"] == product["id"]:
            raise ValueError("Product with this ID already exists")

    data["products"].append(product)

    # Update metadata
    data["metadata"]["totalProducts"] = len(data["products"])
    data["metadata"]["lastUpdated"] = date.today().isoformat()

    save_data(data)

    return product

# DELETE PRODUCTS


def delete_product(product_id:str):
    try:
        data = load_data()
        for indx , product in enumerate(data["products"]):
            if product["id"]==product_id:
                delete_products = data["products"].pop(indx)
                save_data(data)
                return delete_products
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="product id does not exits"
            
        )
    except Exception as e:
        raise ValueError(f"Failed to delete product: {e}")