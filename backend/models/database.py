from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'smartbiz.db')}"
engine       = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base         = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Store(Base):
    __tablename__ = "stores"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=True)  # auth bilan bog'liq
    name       = Column(String(100), nullable=False)
    store_type = Column(String(50),  default="dokon")
    address    = Column(String(200))
    phone      = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active  = Column(Boolean,  default=True)

    sales    = relationship("Sale",    back_populates="store", cascade="all, delete")
    products = relationship("Product", back_populates="store", cascade="all, delete")
    debts    = relationship("Debt",    back_populates="store", cascade="all, delete")


class Sale(Base):
    __tablename__ = "sales"
    id             = Column(Integer, primary_key=True, index=True)
    store_id       = Column(Integer, ForeignKey("stores.id"), nullable=False)
    date           = Column(Date, nullable=False)
    total_amount   = Column(Float, default=0)
    cash_amount    = Column(Float, default=0)
    card_amount    = Column(Float, default=0)
    expenses       = Column(Float, default=0)
    profit         = Column(Float, default=0)
    customer_count = Column(Integer, default=0)
    note           = Column(Text)
    created_at     = Column(DateTime, default=datetime.utcnow)

    store      = relationship("Store",    back_populates="sales")
    sale_items = relationship("SaleItem", back_populates="sale", cascade="all, delete")


class SaleItem(Base):
    __tablename__ = "sale_items"
    id         = Column(Integer, primary_key=True, index=True)
    sale_id    = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    name       = Column(String(100))
    quantity   = Column(Float, default=0)
    unit       = Column(String(20), default="dona")
    unit_price = Column(Float, default=0)
    total      = Column(Float, default=0)

    sale    = relationship("Sale",    back_populates="sale_items")
    product = relationship("Product", back_populates="sale_items")


class Product(Base):
    __tablename__ = "products"
    id           = Column(Integer, primary_key=True, index=True)
    store_id     = Column(Integer, ForeignKey("stores.id"), nullable=False)
    name         = Column(String(100), nullable=False)
    category     = Column(String(50),  default="umumiy")
    unit         = Column(String(20),  default="dona")
    quantity     = Column(Float, default=0)
    min_quantity = Column(Float, default=5)
    buy_price    = Column(Float, default=0)
    sell_price   = Column(Float, default=0)
    created_at   = Column(DateTime, default=datetime.utcnow)

    store      = relationship("Store",    back_populates="products")
    sale_items = relationship("SaleItem", back_populates="product")


class Debt(Base):
    __tablename__ = "debts"
    id          = Column(Integer, primary_key=True, index=True)
    store_id    = Column(Integer, ForeignKey("stores.id"), nullable=False)
    person_name = Column(String(100), nullable=False)
    phone       = Column(String(20))
    debt_type   = Column(String(20), default="mijoz")
    amount      = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0)
    due_date    = Column(Date)
    is_paid     = Column(Boolean, default=False)
    note        = Column(Text)
    created_at  = Column(DateTime, default=datetime.utcnow)

    store = relationship("Store", back_populates="debts")


def init_db():
    Base.metadata.create_all(bind=engine)


