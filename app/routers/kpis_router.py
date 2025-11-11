from datetime import datetime, time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from .. import schemas
from ..deps import get_db, get_current_user
from ..models import Receipt, ReceiptLine, Product, Shop, User

router = APIRouter(prefix="/shops/{shop_id}/kpis", tags=["kpis"])


def _ensure_shop_owner(
    db: Session,
    shop_id: int,
    user: User,
) -> Shop:
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found",
        )
    if shop.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this shop",
        )
    return shop


def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        # Interpretamos YYYY-MM-DD al inicio del día
        d = datetime.fromisoformat(date_str).date()
        return datetime.combine(d, time.min)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format, expected YYYY-MM-DD",
        )


@router.get("", response_model=schemas.KPIs)
def get_kpis(
    shop_id: int,
    from_date: Optional[str] = Query(
        None, alias="from", description="YYYY-MM-DD (inclusive)"
    ),
    to_date: Optional[str] = Query(
        None, alias="to", description="YYYY-MM-DD (inclusive)"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _ensure_shop_owner(db, shop_id, current_user)

    start_dt = _parse_date(from_date)
    end_dt = _parse_date(to_date)

    # Ajuste para incluir todo el día en 'to'
    if end_dt is not None:
        end_dt = end_dt.replace(hour=23, minute=59, second=59, microsecond=999999)

    # ---- total_receipts & total_revenue ----
    receipts_query = db.query(Receipt).filter(Receipt.shop_id == shop_id)

    if start_dt is not None:
        receipts_query = receipts_query.filter(Receipt.created_at >= start_dt)
    if end_dt is not None:
        receipts_query = receipts_query.filter(Receipt.created_at <= end_dt)

    total_receipts = receipts_query.count()
    total_revenue = (
        db.query(func.coalesce(func.sum(Receipt.total), 0))
        .filter(Receipt.shop_id == shop_id)
        .filter(
            *([Receipt.created_at >= start_dt] if start_dt is not None else []),
            *([Receipt.created_at <= end_dt] if end_dt is not None else []),
        )
        .scalar()
    )

    # ---- top_skus ----
    lines_query = (
        db.query(
            Product.sku.label("sku"),
            Product.name.label("name"),
            func.sum(ReceiptLine.qty).label("qty"),
            func.sum(ReceiptLine.qty * ReceiptLine.unit_price).label("revenue"),
        )
        .join(Receipt, ReceiptLine.receipt_id == Receipt.id)
        .join(Product, ReceiptLine.product_id == Product.id)
        .filter(Receipt.shop_id == shop_id)
    )

    if start_dt is not None:
        lines_query = lines_query.filter(Receipt.created_at >= start_dt)
    if end_dt is not None:
        lines_query = lines_query.filter(Receipt.created_at <= end_dt)

    lines_query = (
        lines_query.group_by(Product.id, Product.sku, Product.name)
        .order_by(desc("qty"))
        .limit(5)
    )

    top_skus = [
        schemas.TopSku(
            sku=row.sku,
            name=row.name,
            qty=int(row.qty),
            revenue=float(row.revenue),
        )
        for row in lines_query.all()
    ]

    return schemas.KPIs(
        shop_id=shop_id,
        total_receipts=int(total_receipts),
        total_revenue=float(total_revenue or 0),
        top_skus=top_skus,
    )
