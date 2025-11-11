from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional


# ---------- Auth ----------


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Shops ----------


class ShopCreate(BaseModel):
    name: str


class ShopOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# ---------- Products ----------


class ProductCreate(BaseModel):
    sku: str
    name: str
    price: float


class ProductOut(BaseModel):
    id: int
    sku: str
    name: str
    price: float

    model_config = ConfigDict(from_attributes=True)


# ---------- Receipts ----------


class ReceiptLineIn(BaseModel):
    sku: str
    qty: int
    unit_price: float


class ReceiptIn(BaseModel):
    lines: List[ReceiptLineIn]


class ReceiptOut(BaseModel):
    id: int
    total: float

    model_config = ConfigDict(from_attributes=True)


# ---------- KPIs ----------


class TopSku(BaseModel):
    sku: str
    name: Optional[str] = None
    qty: int
    revenue: float


class KPIs(BaseModel):
    shop_id: int
    total_receipts: int
    total_revenue: float
    top_skus: List[TopSku]
