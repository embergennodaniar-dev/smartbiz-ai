from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db, Store
from models.schemas import StoreCreate, StoreOut
from routers.auth import get_current_user, User
from lang.uz import T
from typing import List

router = APIRouter()

@router.get("/", response_model=List[StoreOut])
def get_stores(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Store).filter(Store.user_id == current_user.id, Store.is_active == True).all()

@router.post("/", response_model=StoreOut)
def create_store(data: StoreCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    store = Store(**data.model_dump(), user_id=current_user.id)
    db.add(store); db.commit(); db.refresh(store)
    return store

@router.put("/{store_id}", response_model=StoreOut)
def update_store(store_id: int, data: StoreCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    store = db.query(Store).filter(Store.id == store_id, Store.user_id == current_user.id).first()
    if not store: raise HTTPException(404, T["store_not_found"])
    for k, v in data.model_dump().items(): setattr(store, k, v)
    db.commit(); db.refresh(store)
    return store

@router.delete("/{store_id}")
def delete_store(store_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    store = db.query(Store).filter(Store.id == store_id, Store.user_id == current_user.id).first()
    if not store: raise HTTPException(404, T["store_not_found"])
    store.is_active = False; db.commit()
    return {"ok": True}
