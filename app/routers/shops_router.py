from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas
from ..deps import get_db, get_current_user
from ..models import Shop, User

router = APIRouter(prefix="/shops", tags=["shops"])


@router.post(
    "",
    response_model=schemas.ShopOut,
    status_code=status.HTTP_201_CREATED,
)
def create_shop(
    shop_in: schemas.ShopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    shop = Shop(name=shop_in.name, owner_id=current_user.id)
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop
