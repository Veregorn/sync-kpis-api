from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas
from ..deps import get_db, get_current_user
from ..models import Product, User

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    "",
    response_model=schemas.ProductOut,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_in: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Para el MVP no limitamos por usuario: catálogo global.
    existing = db.query(Product).filter(Product.sku == product_in.sku).first()
    if existing:
        return existing

    product = Product(
        sku=product_in.sku,
        name=product_in.name,
        price=product_in.price,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
