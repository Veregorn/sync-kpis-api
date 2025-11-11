from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..deps import get_db, get_current_user
from ..models import (
    Shop,
    User,
    Product,
    Receipt,
    ReceiptLine,
    IdempotencyKey,
)

router = APIRouter(
    prefix="/shops/{shop_id}/receipts",
    tags=["receipts"],
)


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


@router.post(
    "",
    response_model=schemas.ReceiptOut,
    status_code=status.HTTP_201_CREATED,
)
def create_receipt(
    shop_id: int,
    body: schemas.ReceiptIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    # 1) Validate shop & owner
    _ensure_shop_owner(db, shop_id, current_user)

    # 2) Si hay Idempotency-Key, mirar si ya existe
    if idempotency_key:
        existing = (
            db.query(IdempotencyKey)
            .filter(IdempotencyKey.key == idempotency_key)
            .first()
        )
        if existing and existing.receipt_id is not None:
            # Recover the associated receipt and return it
            receipt = (
                db.query(Receipt).filter(Receipt.id == existing.receipt_id).first()
            )
            if receipt:
                return schemas.ReceiptOut(
                    id=receipt.id,
                    total=float(receipt.total),
                )

    # 3) Create / ensure products + calculate total
    total = 0.0
    lines_models: list[ReceiptLine] = []

    for line in body.lines:
        if line.qty <= 0 or line.unit_price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid qty or unit_price",
            )

        product = db.query(Product).filter(Product.sku == line.sku).first()
        if not product:
            # If not exists, create it on-the-fly with the SKU as name
            product = Product(
                sku=line.sku,
                name=line.sku,
                price=line.unit_price,
            )
            db.add(product)
            db.flush()  # get product.id

        line_total = line.qty * line.unit_price
        total += line_total

        lines_models.append(
            ReceiptLine(
                product_id=product.id,
                qty=line.qty,
                unit_price=line.unit_price,
            )
        )

    # 4) Create receipt + lines in a transaction
    receipt = Receipt(shop_id=shop_id, total=total)
    db.add(receipt)
    db.flush()  # get receipt.id

    for lm in lines_models:
        lm.receipt_id = receipt.id
        db.add(lm)

    # 5) Save Idempotency-Key if applies
    if idempotency_key:
        idem = IdempotencyKey(
            key=idempotency_key,
            receipt_id=receipt.id,
        )
        db.add(idem)

    db.commit()
    db.refresh(receipt)

    return schemas.ReceiptOut(id=receipt.id, total=float(receipt.total))
