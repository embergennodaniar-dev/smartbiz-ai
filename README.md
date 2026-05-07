# SmartBiz AI — Biznes Boshqaruv Tizimi

Big Data + Sun'iy Intellekt yordamida universal biznes tahlil platformasi.

## Loyiha tuzilmasi

```
smartbiz-ai/
├── backend/
│   ├── main.py                  # FastAPI asosiy server
│   ├── models/
│   │   ├── database.py          # SQLite modellari + demo ma'lumotlar
│   │   └── schemas.py           # Pydantic sxemalari
│   └── routers/
│       ├── stores.py            # Do'kon CRUD
│       ├── sales.py             # Savdo CRUD + statistikalar
│       ├── products.py          # Mahsulot + sklad boshqaruvi
│       ├── debts.py             # Qarz daftar
│       ├── analytics.py         # AI tahlil + insights
│       ├── forecast.py          # ML prognoz (linear regression + seasonality)
│       └── upload.py            # CSV fayl yuklash + parser
├── frontend/
│   └── templates/
│       └── index.html           # To'liq SPA (HTML+CSS+JS)
├── requirements.txt
└── run.sh                       # Ishga tushirish skripti
```

## Ishga tushirish

```bash
bash run.sh
# Keyin: http://localhost:8000
```

Yoki qo'lda:
```bash
cd backend
pip install -r ../requirements.txt
python -c "from models.database import init_db; init_db()"
uvicorn main:app --reload --port 8000
```

## Funksiyalar

### Dashboard
- Bugungi / oylik savdo statistikasi
- Haftalik savdo grafigi
- Top va kam sotiladigan mahsulotlar
- AI maslahatlar (real vaqtda)

### Kunlik kiritish
- Savdo summasi (naqd + karta)
- Xarajatlar va sof foyda
- Mahsulot sotuvlari (birma-bir)
- Avtomatik sklad yangilanishi

### Sklad
- Barcha mahsulotlar ro'yxati
- Kam qoldiq ogohlantirishi
- Kirim qilish
- Narx boshqaruvi

### Qarz daftar
- Mijoz qarzlari
- Yetkazuvchi qarzlari
- Muddati o'tgan qarzlar (qizil)
- To'lov qayd etish

### Tahlil (AI)
- Hafta kunlari bo'yicha tahlil
- Soatlik savdo taqsimoti
- Top 10 mahsulot
- AI maslahatlar (avtomatik)

### Prognoz (ML)
- 30 kunlik savdo bashorati
- Linear regression + kunlik seasonality
- Ishonchlilik oralig'i

### Fayl yuklash
- CSV savdo import
- CSV mahsulot import
- Drag & drop qo'llab-quvvatlash
- Shablon fayllari

## Texnologiyalar

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, SQLite
- **Frontend**: Vanilla HTML/CSS/JS, Chart.js
- **ML/AI**: Custom linear regression + seasonality model
- **Ma'lumotlar bazasi**: SQLite (production uchun PostgreSQL ga almashtiring)

## API hujjatlar

Server ishga tushgandan keyin: http://localhost:8000/docs

## Kengaytirish

Production uchun:
1. SQLite → PostgreSQL
2. `AI insights` → OpenAI API ulash
3. Telegram bot qo'shish (qarz eslatmalari)
4. Docker + VPS deploy
