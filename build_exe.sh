#!/bin/bash
# =====================================================
#  SmartBiz AI — EXE yaratish skripti
#  Ishlatish: bash build_exe.sh
# =====================================================

echo ""
echo "  ◈ SmartBiz AI — EXE Builder"
echo "  ================================"
echo ""

# 1. Kutubxonalar
echo "[1/4] Kerakli kutubxonalar o'rnatilmoqda..."
pip install pyinstaller fastapi uvicorn sqlalchemy pydantic \
    python-jose passlib bcrypt python-multipart \
    google-generativeai -q
echo "      OK"

# 2. Eski build fayllar tozalanadi
echo "[2/4] Eski build tozalanmoqda..."
rm -rf build/ dist/ __pycache__/
echo "      OK"

# 3. EXE yaratish
echo "[3/4] EXE yaratilmoqda (3-5 daqiqa ketishi mumkin)..."
echo ""
pyinstaller smartbiz.spec --noconfirm 2>&1 | grep -E "INFO|WARNING|ERROR|Building|Copying" | head -40
echo ""

# 4. Natija
if [ -f "dist/SmartBizAI" ] || [ -f "dist/SmartBizAI.exe" ]; then
    echo "[4/4] Muvaffaqiyat!"
    echo ""
    ls -lh dist/SmartBizAI* 2>/dev/null || ls -lh dist/SmartBizAI.exe 2>/dev/null
    echo ""
    echo "  EXE tayyor: dist/ papkasida"
    echo "  Windows uchun: dist/SmartBizAI.exe"
    echo "  Linux/Mac uchun: dist/SmartBizAI"
    echo ""
    echo "  Ishlatish:"
    echo "    1. dist/SmartBizAI.exe ni ikki marta bosing"
    echo "    2. Brauzer avtomatik ochiladi"
    echo "    3. AI kaliti bo'lmasa — demo rejim ishlaydi"
else
    echo "[4/4] XATO — EXE yaratilmadi"
    echo "      'dist/' papkasini tekshiring"
fi
