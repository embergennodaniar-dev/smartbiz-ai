from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.database import Store

def verify_store_owner(store_id: int, user_id: int, db: Session) -> Store:
    store = db.query(Store).filter(
        Store.id == store_id,
        Store.user_id == user_id,
        Store.is_active == True,
    ).first()
    if not store:
        raise HTTPException(403, "Bu do'konga kirish huquqingiz yo'q")
    return store
