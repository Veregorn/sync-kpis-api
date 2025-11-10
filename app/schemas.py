from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List


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
