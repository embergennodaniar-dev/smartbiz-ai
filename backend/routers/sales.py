from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models.database import get_db, Store, Sale, SaleItem, Product
from models.schemas import SaleCreate, SaleOut
from lang.uz import T
from typing import List, Optional
from datetime import date, timedelta
from routers.auth import get_current_user, User

router = APIRouter()

@router.get("/", response_model=List[SaleOut])
def get_sales(
    store_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(30, le=365),
    db: Session = Depends(get_db)
):
    q = db.query(Sale).filter(Sale.store_id == store_id)
    if start_date:
        q = q.filter(Sale.date >= start_date)
    if end_date:
        q = q.filter(Sale.date <= end_date)
    return q.order_by(desc(Sale.date)).limit(limit).all()

@router.post("/", response_model=SaleOut)
def create_sale(data: SaleCreate, db: Session = Depends(get_db)):
    profit = data.total_amount - data.expenses
    sale = Sale(
        store_id=data.store_id, date=data.date,
        total_amount=data.total_amount, cash_amount=data.cash_amount,
        card_amount=data.card_amount, expenses=data.expenses,
        profit=profit, customer_count=data.customer_count, note=data.note
    )
    db.add(sale)
    db.flush()

    for item in data.items:
        si = SaleItem(sale_id=sale.id, **item.model_dump())
        db.add(si)
        if item.product_id:
            prod = db.query(Product).filter(Product.id == item.product_id).first()
            if prod:
                prod.quantity = max(0, prod.quantity - item.quantity)

    db.commit()
    db.refresh(sale)
    return sale

@router.get("/today")
def today_summary(store_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = date.today()
    yesterday = today - timedelta(days=1)

    t = db.query(func.sum(Sale.total_amount), func.sum(Sale.profit), func.sum(Sale.customer_count))\
          .filter(Sale.store_id == store_id, Sale.date == today).first()
    y = db.query(func.sum(Sale.total_amount))\
          .filter(Sale.store_id == store_id, Sale.date == yesterday).first()

    today_total  = t[0] or 0
    today_profit = t[1] or 0
    today_customers = t[2] or 0
    yesterday_total = y[0] or 1
    change = round(((today_total - yesterday_total) / yesterday_total) * 100, 1)

    return {
        "total": today_total, "profit": today_profit,
        "customers": today_customers, "change_pct": change,
        "yesterday": yesterday_total
    }

@router.get("/weekly")
def weekly_sales(store_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    end   = date.today()
    start = end - timedelta(days=6)
    rows = db.query(Sale.date, func.sum(Sale.total_amount), func.sum(Sale.profit))\
             .filter(Sale.store_id == store_id, Sale.date >= start)\
             .group_by(Sale.date).order_by(Sale.date).all()
    return [{"date": str(r[0]), "total": r[1] or 0, "profit": r[2] or 0} for r in rows]

@router.get("/monthly-summary")
def monthly_summary(store_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = date.today()
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_end   = this_month_start - timedelta(days=1)

    def agg(start, end):
        r = db.query(func.sum(Sale.total_amount), func.sum(Sale.profit), func.sum(Sale.customer_count))\
              .filter(Sale.store_id == store_id, Sale.date >= start, Sale.date <= end).first()
        return r[0] or 0, r[1] or 0, r[2] or 0

    cur_total, cur_profit, cur_customers = agg(this_month_start, today)
    prv_total, prv_profit, _             = agg(last_month_start, last_month_end)
    change = round(((cur_total - prv_total) / max(prv_total, 1)) * 100, 1)
    return {
        "this_month": cur_total, "this_profit": cur_profit,
        "customers": cur_customers, "change_pct": change,
        "last_month": prv_total
    }

@router.delete("/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(404, T["sale_not_found"])
    db.delete(sale)
    db.commit()
    return {"ok": True}
