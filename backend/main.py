from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from models.database import init_db
from routers import sales, products, debts, analytics, forecast, stores, upload
from routers.auth import router as auth_router
from routers.ai import router as ai_router
import os
from lang.uz import T, f
app = FastAPI(title="SmartBiz AI", version="2.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# DB
init_db()

# Routers
app.include_router(auth_router,      prefix="/api/auth",     tags=["Auth"])
app.include_router(ai_router,         prefix="/api/ai",       tags=["AI"])
app.include_router(stores.router,    prefix="/api/stores",   tags=["Stores"])
app.include_router(sales.router,     prefix="/api/sales",    tags=["Sales"])
app.include_router(products.router,  prefix="/api/products", tags=["Products"])
app.include_router(debts.router,     prefix="/api/debts",    tags=["Debts"])
app.include_router(analytics.router, prefix="/api/analytics",tags=["Analytics"])
app.include_router(forecast.router,  prefix="/api/forecast", tags=["Forecast"])
app.include_router(upload.router,    prefix="/api/upload",   tags=["Upload"])

# Static + SPA
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
static_dir    = os.path.join(frontend_path, "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def _read_html(name: str) -> str:
    path = os.path.join(frontend_path, "templates", name)
    with open(path, encoding="utf-8") as f:
        return f.read()

@app.get("/",        response_class=HTMLResponse)
async def root():   return _read_html("index.html")

@app.get("/login",   response_class=HTMLResponse)
async def login():  return _read_html("auth.html")

@app.get("/register",response_class=HTMLResponse)
async def register():return _read_html("auth.html")

@app.get("/health")
async def health():  return {"status": "ok", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
