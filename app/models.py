from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    DateTime,
    Numeric,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    shops: Mapped[list["Shop"]] = relationship(back_populates="owner")


class Shop(Base):
    __tablename__ = "shops"
    __table_args__ = (UniqueConstraint("owner_id", "name", name="uq_shop_owner_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped[User] = relationship(back_populates="shops")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Numeric(10, 2))


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"), index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    total: Mapped[float] = mapped_column(Numeric(12, 2))

    # Relación bidireccional con ReceiptLine
    lines: Mapped[list["ReceiptLine"]] = relationship(
        back_populates="receipt",
        cascade="all, delete-orphan",
    )


class ReceiptLine(Base):
    __tablename__ = "receipt_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    receipt_id: Mapped[int] = mapped_column(
        ForeignKey("receipts.id", ondelete="CASCADE"),
        index=True,
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    qty: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2))

    receipt: Mapped["Receipt"] = relationship(back_populates="lines")
    # Optional: product: Mapped["Product"] = relationship()


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    receipt_id: Mapped[int | None] = mapped_column(
        ForeignKey("receipts.id"), nullable=True
    )
