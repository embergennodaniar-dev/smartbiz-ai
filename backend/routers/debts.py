from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db, Debt
from models.schemas import DebtCreate, DebtOut, DebtPayment
from pydantic import BaseModel

from typing import List, Optional
from datetime import date

router = APIRouter()

def _enrich(d: Debt) -> dict:
    today = date.today()
    return {
        "id": d.id, "store_id": d.store_id, "person_name": d.person_name,
        "phone": d.phone, "debt_type": d.debt_type, "amount": d.amount,
        "paid_amount": d.paid_amount, "remaining": d.amount - d.paid_amount,
        "due_date": d.due_date, "is_paid": d.is_paid,
        "is_overdue": (d.due_date < today if d.due_date else False) and not d.is_paid,
        "note": d.note
    }

@router.get("/")
def get_debts(store_id: int, debt_type: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Debt).filter(Debt.store_id == store_id, Debt.is_paid == False)
    if debt_type:
        q = q.filter(Debt.debt_type == debt_type)
    return [_enrich(d) for d in q.order_by(Debt.due_date).all()]

@router.get("/summary")
def debt_summary(store_id: int, db: Session = Depends(get_db)):
    debts = db.query(Debt).filter(Debt.store_id == store_id, Debt.is_paid == False).all()
    today = date.today()
    total_mijoz    = sum(d.amount - d.paid_amount for d in debts if d.debt_type == "mijoz")
    total_supplier = sum(d.amount - d.paid_amount for d in debts if d.debt_type == "yetkazuvchi")
    overdue_count  = sum(1 for d in debts if d.due_date and d.due_date < today)
    return {"total_mijoz": total_mijoz, "total_supplier": total_supplier,
            "overdue_count": overdue_count, "total_count": len(debts)}

@router.post("/")
def create_debt(data: DebtCreate, db: Session = Depends(get_db)):
    debt = Debt(**data.model_dump())
    db.add(debt)
    db.commit()
    db.refresh(debt)
    return _enrich(debt)

@router.patch("/{debt_id}/pay")
def pay_debt(debt_id: int, data: DebtPayment, db: Session = Depends(get_db)):
    debt = db.query(Debt).filter(Debt.id == debt_id).first()
    if not debt:
        raise HTTPException(404, T["debt_not_found"])
    debt.paid_amount = min(debt.amount, debt.paid_amount + data.paid_amount)
    if debt.paid_amount >= debt.amount:
        debt.is_paid = True
    db.commit()
    return _enrich(debt)

@router.delete("/{debt_id}")
def delete_debt(debt_id: int, db: Session = Depends(get_db)):
    debt = db.query(Debt).filter(Debt.id == debt_id).first()
    if not debt:
        raise HTTPException(404, T["debt_not_found"])
    db.delete(debt)
    db.commit()
    return {"ok": True}

class NoteUpdate(BaseModel):
    note: str = ""

@router.patch("/{debt_id}/note")
def update_note(debt_id: int, data: NoteUpdate, db: Session = Depends(get_db)):
    debt = db.query(Debt).filter(Debt.id == debt_id).first()
    if not debt:
        raise HTTPException(404, T["debt_not_found"])
    debt.note = data.note
    db.commit()
    return _enrich(debt)

@router.get("/history")
def debt_history(store_id: int, db: Session = Depends(get_db)):
    """To'langan qarzlar tarixi"""
    debts = db.query(Debt).filter(Debt.store_id == store_id, Debt.is_paid == True)               .order_by(Debt.created_at.desc()).limit(50).all()
    return [_enrich(d) for d in debts]
