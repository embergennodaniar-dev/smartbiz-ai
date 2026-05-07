#!/bin/bash
echo "========================================"
echo "  SmartBiz AI v2.0 — AI Powered"
echo "========================================"
cd "$(dirname "$0")"
echo "[1/3] Kutubxonalar o'rnatilmoqda..."
pip install -r requirements.txt -q
echo "[2/3] Ma'lumotlar bazasi tayyorlanmoqda..."
cd backend
python -c "from models.database import init_db; init_db(); print('DB tayyor!')"
echo "[3/3] Server ishga tushirilmoqda..."
echo ""
echo "  Sayt:  http://localhost:8000"
echo "  Docs:  http://localhost:8000/docs"
echo ""
echo "  AI kalit: saytga kirib AI Sozlama bo'limiga o'ting"
echo ""
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
