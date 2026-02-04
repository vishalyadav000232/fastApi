# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal , engine , Base
from app.schemas.schemas import Product , ProductBase , ProductCreate
from app.crud import create_product , get_products


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + PostgreSQL 18 Example with .env")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "FastAPI + PostgreSQL 18 with .env is working!"}

@app.post("/products/", response_model=Product)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@app.get("/products/", response_model=list[Product])
def list_products(db: Session = Depends(get_db)):
    return get_products(db)
