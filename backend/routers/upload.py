from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db, Sale, Product, Debt
from lang.uz import T, f
from datetime import datetime, date
import io, csv

router = APIRouter()


def _parse_num(val):
    try:
        return float(str(val).replace(",", "").replace(" ", "").replace("'", ""))
    except:
        return 0.0


def _parse_date(val):
    for fmt_str in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(str(val).strip(), fmt_str).date()
        except:
            pass
    return date.today()


@router.post("/sales-csv")
async def upload_sales_csv(store_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".csv", ".CSV")):
        raise HTTPException(400, T["csv_only"])

    content = await file.read()
    try:
        text = content.decode("utf-8")
    except:
        text = content.decode("latin-1")

    reader  = csv.DictReader(io.StringIO(text))
    created = 0
    errors  = []

    col_map = {
        "sana":   ["date", "sana", "kun"],
        "total":  ["total", "jami", "summa", "total_amount", "savdo"],
        "naqd":   ["cash", "naqd", "cash_amount"],
        "karta":  ["card", "karta", "card_amount"],
        "xarajat":["expenses", "xarajat"],
        "mijoz":  ["customers", "mijozlar", "customer_count"],
    }

    def find_col(row, keys):
        for k in keys:
            for h in row.keys():
                if h.lower().strip() == k:
                    return h
        return None

    for i, row in enumerate(reader):
        try:
            dc = find_col(row, col_map["sana"])
            tc = find_col(row, col_map["total"])
            if not dc or not tc:
                errors.append(f("upload_row_error", row=i+2, err=T["col_missing"]))
                continue

            total    = _parse_num(row[tc])
            xar_c    = find_col(row, col_map["xarajat"])
            expenses = _parse_num(row[xar_c]) if xar_c else total * 0.3
            naqd_c   = find_col(row, col_map["naqd"])
            karta_c  = find_col(row, col_map["karta"])
            mijoz_c  = find_col(row, col_map["mijoz"])

            sale = Sale(
                store_id=store_id, date=_parse_date(row[dc]),
                total_amount=total,
                cash_amount=_parse_num(row[naqd_c]) if naqd_c else total * 0.6,
                card_amount=_parse_num(row[karta_c]) if karta_c else total * 0.4,
                expenses=expenses, profit=total - expenses,
                customer_count=int(_parse_num(row[mijoz_c])) if mijoz_c else 0,
            )
            db.add(sale)
            created += 1
        except Exception as e:
            errors.append(f("upload_row_error", row=i+2, err=str(e)))

    db.commit()
    return {"imported": created, "errors": errors[:10],
            "message": f("upload_sales_ok", count=created)}


@router.post("/products-csv")
async def upload_products_csv(store_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".csv", ".CSV")):
        raise HTTPException(400, T["csv_only"])

    content = await file.read()
    try:
        text = content.decode("utf-8")
    except:
        text = content.decode("latin-1")

    reader  = csv.DictReader(io.StringIO(text))
    created = 0
    for row in reader:
        try:
            name = (row.get("name") or row.get("nomi") or row.get("mahsulot", "")).strip()
            if not name:
                continue
            prod = Product(
                store_id=store_id, name=name,
                category=row.get("category", row.get("kategoriya", T["prod_cat_food"])).strip(),
                unit=row.get("unit", row.get("olchov", T["prod_unit_dona"])).strip(),
                quantity=_parse_num(row.get("quantity", row.get("miqdori", 0))),
                min_quantity=_parse_num(row.get("min_quantity", row.get("minimum", 5))),
                buy_price=_parse_num(row.get("buy_price", row.get("kirim_narx", 0))),
                sell_price=_parse_num(row.get("sell_price", row.get("sotish_narx", 0))),
            )
            db.add(prod)
            created += 1
        except:
            pass
    db.commit()
    return {"imported": created, "message": f("upload_products_ok", count=created)}


@router.get("/template/sales")
def download_sales_template():
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        io.StringIO(T["csv_sales_sample"]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename={T["csv_sales_filename"]}'},
    )


@router.get("/template/products")
def download_products_template():
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        io.StringIO(T["csv_products_sample"]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename={T["csv_products_filename"]}'},
    )
