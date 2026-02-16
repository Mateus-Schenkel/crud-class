from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schema import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product,
)

router = APIRouter()

### create route to get all items
### we will always have 2 atributes PATH and RESPONSE
@router.get("/products/", response_model=List[ProductResponse])
def read_all_products_route(db: Session = Depends(get_db)):
    products = get_products(db)
    return products

### create route to get 1 item
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Você esta querendo buscar um produto que não existe")
    return db_product

### create route to add 1 item
@router.post("/products/", response_model=ProductResponse)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)

### create route to delete an item
@router.delete("/products/{product_id}", response_model=ProductResponse)
def detele_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = delete_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Você esta querendo deletar um produto que não existe")
    return db_product

### create route to update an item
@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    db_product = update_product(db=db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Você esta querendo atualizar um produto que não existe")
    return db_product