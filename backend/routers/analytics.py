from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models.database import get_db, Store, Sale, SaleItem, Product
from lang.uz import T, f, WEEKDAYS, WEEKDAY_BY_DOW
from datetime import date, timedelta
from routers.auth import get_current_user, User

router = APIRouter()


@router.get("/overview")
def overview(store_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = date.today()
    month_start = today.replace(day=1)
    last_month_start = (month_start - timedelta(days=1)).replace(day=1)
    last_month_end = month_start - timedelta(days=1)

    def get_totals(start, end):
        r = db.query(func.sum(Sale.total_amount), func.sum(Sale.profit), func.sum(Sale.customer_count))\
              .filter(Sale.store_id == store_id, Sale.date.between(start, end)).first()
        return r[0] or 0, r[1] or 0, r[2] or 0

    cur_t, cur_p, cur_c = get_totals(month_start, today)
    prv_t, prv_p, _     = get_totals(last_month_start, last_month_end)

    today_r = db.query(func.sum(Sale.total_amount), func.sum(Sale.profit))\
                .filter(Sale.store_id == store_id, Sale.date == today).first()
    yesterday_r = db.query(func.sum(Sale.total_amount))\
                    .filter(Sale.store_id == store_id, Sale.date == today - timedelta(days=1)).first()

    today_total     = today_r[0] or 0
    yesterday_total = yesterday_r[0] or 1
    day_change      = round(((today_total - yesterday_total) / yesterday_total) * 100, 1)
    month_change    = round(((cur_t - prv_t) / max(prv_t, 1)) * 100, 1)

    low_stock = db.query(Product).filter(Product.store_id == store_id)\
                  .filter(Product.quantity <= Product.min_quantity).count()

    from models.database import Debt
    overdue_debts = db.query(Debt).filter(Debt.store_id == store_id, Debt.is_paid == False)\
                      .filter(Debt.due_date < today).count()
    total_debts = db.query(func.sum(Debt.amount - Debt.paid_amount))\
                    .filter(Debt.store_id == store_id, Debt.is_paid == False).scalar() or 0

    avg_check = round(cur_t / max(cur_c, 1))
    return {
        "today_total": today_total, "today_profit": today_r[1] or 0, "day_change": day_change,
        "month_total": cur_t, "month_profit": cur_p, "month_change": month_change,
        "month_customers": cur_c, "avg_check": avg_check,
        "low_stock_count": low_stock, "overdue_debts": overdue_debts, "total_debt": total_debts,
    }


@router.get("/hourly")
def hourly(store_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sales = db.query(func.sum(Sale.total_amount))\
              .filter(Sale.store_id == store_id, Sale.date >= date.today() - timedelta(days=30)).scalar() or 0
    daily_avg = sales / 30
    pattern = [0.01,0.005,0.005,0.005,0.01,0.03,0.08,0.12,0.10,0.09,0.08,0.12,
               0.13,0.10,0.07,0.06,0.05,0.04,0.03,0.02,0.015,0.01,0.005,0.002]
    return [{"hour": h, "amount": round(daily_avg * pattern[h])} for h in range(24)]


@router.get("/by-weekday")
def by_weekday(store_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.query(func.strftime('%w', Sale.date).label("wd"), func.avg(Sale.total_amount))\
             .filter(Sale.store_id == store_id).group_by("wd").all()
    result = {str((int(r[0]) + 6) % 7): r[1] or 0 for r in rows}
    return [{"day": WEEKDAYS[i], "avg": round(result.get(str(i), 0))} for i in range(7)]


@router.get("/top-products")
def top_products(store_id: int, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.query(SaleItem.name, func.sum(SaleItem.quantity), func.sum(SaleItem.total))\
             .join(SaleItem.sale).filter(SaleItem.sale.has(store_id=store_id))\
             .group_by(SaleItem.name).order_by(desc(func.sum(SaleItem.total))).limit(limit).all()
    if not rows:
        return [
            {"name": T["prod_bread"],   "quantity": 850, "revenue": 4_250_000, "rank": 1},
            {"name": T["prod_milk"],    "quantity": 320, "revenue": 3_840_000, "rank": 2},
            {"name": T["prod_meat"],    "quantity": 95,  "revenue": 7_125_000, "rank": 3},
            {"name": T["prod_sugar"],   "quantity": 280, "revenue": 3_920_000, "rank": 4},
            {"name": T["prod_oil"],     "quantity": 110, "revenue": 3_850_000, "rank": 5},
        ]
    return [{"name": r[0], "quantity": round(r[1] or 0), "revenue": round(r[2] or 0), "rank": i+1}
            for i, r in enumerate(rows)]


@router.get("/slow-products")
def slow_products(store_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    all_prods  = db.query(Product).filter(Product.store_id == store_id).all()
    sold_names = {r[0] for r in db.query(SaleItem.name)
                   .join(SaleItem.sale).filter(SaleItem.sale.has(store_id=store_id)).all()}
    slow = [{"name": p.name, "quantity": p.quantity, "sell_price": p.sell_price}
            for p in all_prods if p.name not in sold_names or p.quantity > p.min_quantity * 3]
    return slow[:5] if slow else [
        {"name": T["prod_cheese"],  "quantity": 2, "sell_price": 90_000},
        {"name": T["prod_sausage"], "quantity": 4, "sell_price": 68_000},
        {"name": T["prod_fish"],    "quantity": 6, "sell_price": 55_000},
    ]


@router.get("/ai-insights")
def ai_insights(store_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today    = date.today()
    insights = []

    # 1. Low stock products
    low = db.query(Product).filter(Product.store_id == store_id)\
            .filter(Product.quantity <= Product.min_quantity).all()
    for p in low[:3]:
        insights.append({
            "type": "warning", "icon": "warning", "priority": 1,
            "title": f("insight_stock_low_title", name=p.name),
            "text":  f("insight_stock_low_text", qty=p.quantity, unit=p.unit, min_qty=p.min_quantity),
        })

    # 2. Overdue debts
    from models.database import Debt
    overdue = db.query(Debt).filter(Debt.store_id == store_id, Debt.is_paid == False)\
                .filter(Debt.due_date < today).all()
    for d in overdue[:2]:
        insights.append({
            "type": "danger", "icon": "debt", "priority": 2,
            "title": f("insight_debt_overdue_title", person=d.person_name),
            "text":  f("insight_debt_overdue_text", amount=f"{d.amount - d.paid_amount:,.0f}"),
        })

    # 3. Best weekday
    rows = db.query(func.strftime('%w', Sale.date), func.avg(Sale.total_amount))\
             .filter(Sale.store_id == store_id)\
             .group_by(func.strftime('%w', Sale.date)).all()
    if rows:
        best     = max(rows, key=lambda r: r[1] or 0)
        day_name = WEEKDAY_BY_DOW.get(int(best[0]), T["day_fri"])
        insights.append({
            "type": "success", "icon": "trend", "priority": 3,
            "title": f("insight_best_day_title", day=day_name),
            "text":  f("insight_best_day_text", avg=f"{best[1]:,.0f}"),
        })

    # 4. Growth or drop
    this_week = db.query(func.sum(Sale.total_amount))\
                  .filter(Sale.store_id == store_id, Sale.date >= today - timedelta(days=7)).scalar() or 0
    last_week = db.query(func.sum(Sale.total_amount))\
                  .filter(Sale.store_id == store_id,
                          Sale.date.between(today - timedelta(days=14), today - timedelta(days=8))).scalar() or 1
    growth = round(((this_week - last_week) / last_week) * 100, 1)
    if growth > 0:
        insights.append({"type":"success","icon":"growth","priority":4,
            "title": f("insight_growth_title", pct=growth), "text": T["insight_growth_text"]})
    elif growth < -5:
        insights.append({"type":"warning","icon":"drop","priority":4,
            "title": f("insight_drop_title", pct=abs(growth)), "text": T["insight_drop_text"]})

    # 5. General tip
    insights.append({"type":"info","icon":"tip","priority":5,
        "title": T["insight_top_products_title"], "text": T["insight_top_products_text"]})

    return sorted(insights, key=lambda x: x["priority"])
