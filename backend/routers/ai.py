import os, json, random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models.database import get_db, Sale, Product, Debt, Store
from routers.auth import get_current_user, User
from lang.uz import T, f
from demo import get_chat_answer, get_quick_insights, get_monthly_report
from pydantic import BaseModel
from datetime import date, timedelta
from typing import Optional

router = APIRouter()


# ── Gemini (qátelik bolsa demo rejimge ótedi) ────────────────
def _call_gemini(api_key: str, prompt: str) -> str:
    """
    Gemini ǵa soraw jiberedi.
    Qátelik bolsa None qaytaradı — caller demo rejimge ótedi.
    """
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={"temperature": 0.7, "max_output_tokens": 1024},
        )
        result = model.generate_content(prompt)
        return result.text.strip()
    except Exception:
        return None   # ← qátelik → demo rejim, paydalanıwshı sezbesin


# ── Context builder ─────────────────────────────────────────
def _build_context(store_id: int, db: Session) -> dict:
    today = date.today()
    month_start = today.replace(day=1)
    store = db.query(Store).filter(Store.id == store_id).first()

    today_s  = db.query(func.sum(Sale.total_amount), func.sum(Sale.profit))\
                 .filter(Sale.store_id == store_id, Sale.date == today).first()
    monthly  = db.query(func.sum(Sale.total_amount), func.sum(Sale.profit),
                         func.sum(Sale.customer_count))\
                 .filter(Sale.store_id == store_id, Sale.date >= month_start).first()
    last_30  = db.query(Sale.date, Sale.total_amount)\
                 .filter(Sale.store_id == store_id,
                         Sale.date >= today - timedelta(days=30))\
                 .order_by(Sale.date).all()
    low_stk  = db.query(Product)\
                 .filter(Product.store_id == store_id,
                         Product.quantity <= Product.min_quantity).all()
    overdue  = db.query(Debt)\
                 .filter(Debt.store_id == store_id,
                         Debt.is_paid == False, Debt.due_date < today).all()
    total_debt = db.query(func.sum(Debt.amount - Debt.paid_amount))\
                   .filter(Debt.store_id == store_id, Debt.is_paid == False).scalar() or 0

    wd_rows  = db.query(func.strftime('%w', Sale.date),
                         func.avg(Sale.total_amount))\
                 .filter(Sale.store_id == store_id)\
                 .group_by(func.strftime('%w', Sale.date)).all()
    best_wd  = max(wd_rows, key=lambda r: r[1] or 0) if wd_rows else None
    days     = {0:"Ekshembi",1:"Dúyshembi",2:"Siyshembi",
                3:"Sárshembi",4:"Piyshembi",5:"Juma",6:"Shembi"}

    return {
        "store_name":       store.name if store else "Dúkan",
        "today_total":      round(today_s[0] or 0),
        "today_profit":     round(today_s[1] or 0),
        "monthly_total":    round(monthly[0] or 0),
        "monthly_profit":   round(monthly[1] or 0),
        "monthly_customers":int(monthly[2] or 0),
        "avg_daily":        round((monthly[0] or 0) / max(today.day, 1)),
        "low_stock":        [{"name":p.name,"qty":p.quantity,"unit":p.unit} for p in low_stk],
        "overdue_debts":    [{"name":d.person_name,"amount":d.amount-d.paid_amount} for d in overdue],
        "total_debt":       round(total_debt),
        "best_weekday":     days.get(int(best_wd[0]),"") if best_wd else "",
        "best_weekday_avg": round(best_wd[1] or 0) if best_wd else 0,
        "last_7_days":      [{"date":str(r[0]),"amount":round(r[1])} for r in last_30[-7:]],
    }


def _ctx_to_text(ctx: dict) -> str:
    lines = [
        f"Dúkan: {ctx['store_name']}",
        f"Búgingi sawda: {ctx['today_total']:,} sum (payda: {ctx['today_profit']:,} sum)",
        f"Aylıq sawda: {ctx['monthly_total']:,} sum",
        f"Kúnlik ortasha: {ctx['avg_daily']:,} sum",
        f"Aylıq qarıydarlar: {ctx['monthly_customers']} ta",
        f"Eń aktiv kún: {ctx['best_weekday']}",
        f"Ulıwma qarız: {ctx['total_debt']:,} sum",
    ]
    if ctx["low_stock"]:
        items = ", ".join(f"{p['name']} ({p['qty']} {p['unit']})" for p in ctx["low_stock"])
        lines.append(f"Kem qalǵan: {items}")
    if ctx["overdue_debts"]:
        items = ", ".join(f"{d['name']} ({d['amount']:,.0f} sum)" for d in ctx["overdue_debts"])
        lines.append(f"Múddeti ótken qarızlar: {items}")
    return "\n".join(lines)


# ── Schemas ──────────────────────────────────────────────────
class ChatRequest(BaseModel):
    store_id: int
    question: str
    api_key:  Optional[str] = None

class StoreRequest(BaseModel):
    store_id: int
    api_key:  Optional[str] = None

class KeyRequest(BaseModel):
    api_key: str


# ── Endpoints ─────────────────────────────────────────────────

@router.post("/chat")
async def ai_chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ctx    = _build_context(data.store_id, db)
    source = "demo"
    answer = None

    api_key = data.api_key or os.getenv("GEMINI_API_KEY", "")
    if api_key:
        prompt = (
            f"{T['ai_system_prompt']}\n\n"
            f"Biznes maǵlıwmatları:\n{_ctx_to_text(ctx)}\n\n"
            f"Soraw: {data.question}"
        )
        answer = _call_gemini(api_key, prompt)
        if answer:
            source = "gemini"

    # Gemini islemese yaki gilit joq → demo
    if not answer:
        answer = get_chat_answer(data.question)

    return {"answer": answer, "source": source, "context": ctx}


@router.post("/quick-insights")
async def ai_quick_insights(
    data: StoreRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ctx    = _build_context(data.store_id, db)
    source = "demo"
    tips   = None

    api_key = data.api_key or os.getenv("GEMINI_API_KEY", "")
    if api_key:
        prompt = (
            f"{T['ai_system_prompt']}\n\n"
            f"{_ctx_to_text(ctx)}\n\n"
            "Tek 3 eń áhmiyetli, ámeliy másláhát ber. "
            "Hár birin jańa qatardan jaz. Basında san bolmasın."
        )
        result = _call_gemini(api_key, prompt)
        if result:
            tips   = [t.strip() for t in result.split("\n") if t.strip()][:3]
            source = "gemini"

    if not tips:
        tips = get_quick_insights()

    return {"tips": tips, "source": source, "context": ctx}


@router.post("/report")
async def ai_report(
    data: StoreRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ctx    = _build_context(data.store_id, db)
    source = "demo"
    report = None

    api_key = data.api_key or os.getenv("GEMINI_API_KEY", "")
    if api_key:
        prompt = f(
            "ai_report_prompt",
            data=_ctx_to_text(ctx)
        )
        result = _call_gemini(api_key, prompt)
        if result:
            report = result
            source = "gemini"

    if not report:
        report = get_monthly_report()

    return {"report": report, "source": source,
            "generated_at": str(date.today()), "context": ctx}


@router.get("/context/{store_id}")
async def get_context(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _build_context(store_id, db)


@router.post("/validate-key")
async def validate_key(data: KeyRequest):
    result = _call_gemini(data.api_key, "Sálem! Tek 'OK' dep juwap ber.")
    if result:
        return {"valid": True, "response": result}
    return {"valid": False, "error": "Gilt nadurıs yaki limit tawsılǵan"}