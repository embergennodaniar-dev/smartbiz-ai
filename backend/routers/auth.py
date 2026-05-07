from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from models.database import get_db, Base, engine, Store, SessionLocal
from lang.uz import T
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

# ── Config ──────────────────────────────────────────────────
SECRET_KEY  = os.getenv("SECRET_KEY", "smartbiz-secret-key-change-in-production-2025")
ALGORITHM   = "HS256"
TOKEN_DAYS  = 7

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2  = OAuth2PasswordBearer(tokenUrl="/api/auth/login-form", auto_error=False)
router  = APIRouter()


# ── User model ───────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True, index=True)
    full_name  = Column(String(100), nullable=False)
    email      = Column(String(150), unique=True, index=True, nullable=False)
    hashed_pw  = Column(String(200), nullable=False)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)


# ── Schemas ──────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    full_name:  str
    email:      str
    password:   str
    store_name: str
    store_type: str = "dokon"

class LoginRequest(BaseModel):
    email:    str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user_name:    str
    user_email:   str


# ── Helpers ───────────────────────────────────────────────────
def hash_pw(pw: str) -> str:
    return pwd_ctx.hash(pw)

def verify_pw(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def make_token(user_id: int, email: str) -> str:
    expire = datetime.utcnow() + timedelta(days=TOKEN_DAYS)
    return jwt.encode({"sub": str(user_id), "email": email, "exp": expire}, SECRET_KEY, ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, T["not_authenticated"])
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, T["token_invalid"])
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, T["token_invalid"])
    return user


# ── Endpoints ─────────────────────────────────────────────────
@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(400, T["email_exists"])

    user = User(
        full_name=data.full_name,
        email=data.email.lower(),
        hashed_pw=hash_pw(data.password),
    )
    db.add(user)
    db.flush()

    store = Store(
        name=data.store_name,
        store_type=data.store_type,
        user_id=user.id,
    )
    db.add(store)
    db.commit()

    return TokenResponse(
        access_token=make_token(user.id, user.email),
        user_name=user.full_name,
        user_email=user.email,
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_pw(data.password, user.hashed_pw):
        raise HTTPException(400, T["invalid_credentials"])

    return TokenResponse(
        access_token=make_token(user.id, user.email),
        user_name=user.full_name,
        user_email=user.email,
    )


@router.post("/login-form")
def login_form(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username.lower()).first()
    if not user or not verify_pw(form.password, user.hashed_pw):
        raise HTTPException(400, T["invalid_credentials"])
    return {"access_token": make_token(user.id, user.email), "token_type": "bearer"}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }
