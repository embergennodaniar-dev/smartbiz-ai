from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class StoreCreate(BaseModel):
    name: str
    store_type: str = "dokon"
    address: Optional[str] = None
    phone: Optional[str] = None

class StoreOut(BaseModel):
    id: int
    name: str
    store_type: str
    address: Optional[str]
    phone: Optional[str]
    created_at: datetime
    class Config: from_attributes = True


class SaleItemCreate(BaseModel):
    product_id: Optional[int] = None
    name: str
    quantity: float
    unit: str = "dona"
    unit_price: float = 0
    total: float = 0

class SaleCreate(BaseModel):
    store_id: int
    date: date
    total_amount: float
    cash_amount: float = 0
    card_amount: float = 0
    expenses: float = 0
    customer_count: int = 0
    note: Optional[str] = None
    items: List[SaleItemCreate] = []

class SaleOut(BaseModel):
    id: int
    store_id: int
    date: date
    total_amount: float
    cash_amount: float
    card_amount: float
    expenses: float
    profit: float
    customer_count: int
    note: Optional[str]
    created_at: datetime
    class Config: from_attributes = True


class ProductCreate(BaseModel):
    store_id: int
    name: str
    category: str = "umumiy"
    unit: str = "dona"
    quantity: float = 0
    min_quantity: float = 5
    buy_price: float = 0
    sell_price: float = 0

class ProductUpdate(BaseModel):
    quantity: Optional[float] = None
    min_quantity: Optional[float] = None
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None

class ProductOut(BaseModel):
    id: int
    store_id: int
    name: str
    category: str
    unit: str
    quantity: float
    min_quantity: float
    buy_price: float
    sell_price: float
    is_low: bool = False
    class Config: from_attributes = True


class DebtCreate(BaseModel):
    store_id: int
    person_name: str
    phone: Optional[str] = None
    debt_type: str = "mijoz"
    amount: float
    paid_amount: float = 0
    due_date: Optional[date] = None
    note: Optional[str] = None

class DebtPayment(BaseModel):
    paid_amount: float

class DebtOut(BaseModel):
    id: int
    store_id: int
    person_name: str
    phone: Optional[str]
    debt_type: str
    amount: float
    paid_amount: float
    remaining: float = 0
    due_date: Optional[date]
    is_paid: bool
    is_overdue: bool = False
    note: Optional[str]
    class Config: from_attributes = True
