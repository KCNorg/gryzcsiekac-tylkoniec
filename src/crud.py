from datetime import datetime
from typing import Optional, Type

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import Order, OrderCategory, OrderStatus, User, UserSession
from src.schemas import (CreateUserSession, LoginRequest, OrderCreate,
                         OrderUpdate, RegisterRequest, UserCreate, UserUpdate)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[User]]:
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


def create_user_session(db: Session, user_session: CreateUserSession) -> UserSession:
    db_user_session = UserSession(**user_session.model_dump())
    db.add(db_user_session)
    db.commit()
    db.refresh(db_user_session)
    return db_user_session


def get_user_session(db: Session, token: str) -> UserSession:
    return db.query(UserSession).filter(UserSession.token == token).first()


def get_orders(
    db: Session,
    category: OrderCategory = None,
    valid_since: datetime = None,
    valid_until: datetime = None,
    status: OrderStatus = None,
    senior_id: int = None,
    volunteer_id: int = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = None,
    sort_direction: str = "asc",
    latitude: str = None,
    longitude: str = None,
) -> list:
    if latitude is None and longitude is None:
        query = db.query(Order)
    else:
        query = db.query(Order).join(User, Order.senior_id == User.id)

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

    if latitude is not None and longitude is not None:
        latitude = float(latitude) if latitude else None
        longitude = float(longitude) if longitude else None

        distance = (
            func.acos(
                func.sin(func.radians(latitude)) * func.sin(func.radians(User.latitude))
                + func.cos(func.radians(latitude))
                * func.cos(func.radians(User.latitude))
                * func.cos(func.radians(User.longitude) - func.radians(longitude))
            )
            * 6371
        )  # Radius of Earth in kilometers
        query = query.add_columns(distance.label("distance"))

    if sort_by:
        if sort_by == "distance" and latitude is not None and longitude is not None:
            if sort_direction == "desc":
                query = query.order_by(distance.desc())
            else:
                query = query.order_by(distance.asc())
        else:
            if sort_direction == "desc":
                query = query.order_by(getattr(Order, sort_by).desc())
            else:
                query = query.order_by(getattr(Order, sort_by).asc())

    results = query.offset(skip).limit(limit).all()

    if latitude is None or longitude is None:
        return results

    orders_with_distance = []
    for result in results:
        order = result[0]
        order_dict = order.__dict__
        if len(result) > 1:
            order_dict["distance"] = result[1]
        orders_with_distance.append(order_dict)

    return orders_with_distance


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


def register_user(db: Session, request: RegisterRequest) -> User:
    db_user = create_user(db, request.to_user_create())
    user_session = CreateUserSession(user_id=db_user.id, token=request.token)
    create_user_session(db, user_session)
    return db_user


def login_user(db: Session, request: LoginRequest) -> Type[User]:
    db_user = get_user_by_phone_number(db, request.phone_number)
    user_session = get_user_session(db, request.token)
    if db_user is None or user_session is None or user_session.user_id != db_user.id:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
