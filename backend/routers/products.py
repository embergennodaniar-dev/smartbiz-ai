from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models.database import get_db, Product, SaleItem
from models.schemas import ProductCreate, ProductUpdate, ProductOut
from lang.uz import T
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ProductOut])
def get_products(store_id: int, db: Session = Depends(get_db)):
    prods = db.query(Product).filter(Product.store_id == store_id).all()
    result = []
    for p in prods:
        d = ProductOut.model_validate(p)
        d.is_low = p.quantity <= p.min_quantity
        result.append(d)
    return result

@router.get("/low-stock")
def low_stock(store_id: int, db: Session = Depends(get_db)):
    prods = db.query(Product).filter(Product.store_id == store_id).all()
    return [{"id": p.id, "name": p.name, "quantity": p.quantity, "min_quantity": p.min_quantity, "unit": p.unit}
            for p in prods if p.quantity <= p.min_quantity]

@router.get("/top-selling")
def top_selling(store_id: int, limit: int = 10, db: Session = Depends(get_db)):
    rows = db.query(SaleItem.name, func.sum(SaleItem.quantity).label("qty"), func.sum(SaleItem.total).label("rev"))\
             .join(SaleItem.sale)\
             .filter(SaleItem.sale.has(store_id=store_id))\
             .group_by(SaleItem.name).order_by(desc("rev")).limit(limit).all()
    return [{"name": r[0], "quantity": r[1] or 0, "revenue": r[2] or 0} for r in rows]

@router.post("/", response_model=ProductOut)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    prod = Product(**data.model_dump())
    db.add(prod)
    db.commit()
    db.refresh(prod)
    out = ProductOut.model_validate(prod)
    out.is_low = prod.quantity <= prod.min_quantity
    return out

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(404, T["product_not_found"])
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(prod, k, v)
    db.commit()
    db.refresh(prod)
    out = ProductOut.model_validate(prod)
    out.is_low = prod.quantity <= prod.min_quantity
    return out

@router.patch("/{product_id}/stock")
def adjust_stock(product_id: int, quantity: float, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(404, T["product_not_found"])
    prod.quantity = max(0, prod.quantity + quantity)
    db.commit()
    return {"id": prod.id, "name": prod.name, "quantity": prod.quantity}

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(404, T["product_not_found"])
    db.delete(prod)
    db.commit()
    return {"ok": True}
