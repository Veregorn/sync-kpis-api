from pydantic import BaseModel, EmailStr, ConfigDict


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
