from datetime import datetime
from typing import Optional, Type

from sqlalchemy.orm import Session

from src.models import Order, OrderCategory, OrderStatus, User
from src.schemas import OrderCreate, OrderUpdate, UserCreate, UserUpdate


def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[Type[User]]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> Optional[Type[User]]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_phone_number(db: Session, phone_number: str) -> Optional[Type[User]]:
    return db.query(User).filter(User.phone_number == phone_number).first()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
        db: Session, user_update: UserUpdate, db_user: Type[User]
) -> Type[User]:
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_orders(
        db: Session,
        category: OrderCategory = None,
        valid_since: datetime = None,
        valid_until: datetime = None,
        status: OrderStatus = None,
        senior_id: int = None,
        volunteer_id: int = None,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = None,
        sort_direction: str = "asc"
) -> list:
    query = db.query(Order)

    if category:
        query = query.filter(Order.category == category)
    if valid_since:
        query = query.filter(Order.valid_since >= valid_since)
    if valid_until:
        query = query.filter(Order.valid_until <= valid_until)
    if status:
        query = query.filter(Order.status == status)
    if senior_id:
        query = query.filter(Order.senior_id == senior_id)
    if volunteer_id:
        query = query.filter(Order.volunteer_id == volunteer_id)
    if sort_by:
        if sort_direction == "desc":
            query = query.order_by(getattr(Order, sort_by).desc())
        else:
            query = query.order_by(getattr(Order, sort_by).asc())

    return query.offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int) -> Optional[Type[Order]]:
    return db.query(Order).filter(Order.id == order_id).first()


def create_order(db: Session, order: OrderCreate) -> Order:
    order = order.model_dump()
    order["created_at"] = datetime.now()
    db_order = Order(**order)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(
        db: Session, order_update: OrderUpdate, db_order: Type[Order]
) -> Type[Order]:
    update_data = order_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order
