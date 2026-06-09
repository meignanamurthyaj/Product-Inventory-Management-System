from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth
from ..database import get_db

router = APIRouter(prefix="/products", tags=['Products'])

@router.get("/", response_model=List[schemas.ProductResponse])
def get_all_products(
    skip: int = Query(0, description="Pagination offset"),
    limit: int = Query(10, description="Pagination limit"),
    category: Optional[str] = Query(None, description="Filter by category"),
    sort_by_price: Optional[str] = Query(None, description="Sort by price: 'asc' or 'desc'"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category == category)
    if sort_by_price == "asc":
        query = query.order_by(models.Product.price.asc())
    elif sort_by_price == "desc":
        query = query.order_by(models.Product.price.desc())
        
    return query.offset(skip).limit(limit).all()

@router.get("/search", response_model=List[schemas.ProductResponse])
def search_products(name: str, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.name.ilike(f"%{name}%")).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# --- PROTECTED ROUTES BELOW ---
@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth.get_current_user)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth.get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.patch("/{product_id}/stock", response_model=schemas.ProductResponse)
def update_stock(product_id: int, stock: schemas.StockUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth.get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.quantity = stock.quantity
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth.get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return None