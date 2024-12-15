from datetime import datetime
from typing import Dict

from pydantic import BaseModel

from src.models import OrderCategory, OrderStatus, UserType


class UserBase(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    address: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    type: UserType
    image_url: str | None = None
    description: str | None = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    type: str | None = None
    image_url: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True


class UserSessionBase(BaseModel):
    token: str
    user_id: int

    class Config:
        from_attributes = True


class CreateUserSession(UserSessionBase):
    pass


class UserSession(UserSessionBase):
    id: int


class OrderBase(BaseModel):
    category: OrderCategory
    description: Dict = {}
    valid_since: datetime
    valid_until: datetime
    status: OrderStatus = OrderStatus.PENDING
    senior_id: int
    volunteer_id: int | None = None

    class Config:
        from_attributes = True


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    category: OrderCategory | None = None
    description: Dict | None = None
    valid_since: datetime | None = None
    valid_until: datetime | None = None
    status: OrderStatus | None = None
    senior_id: int | None = None
    volunteer_id: int | None = None

    class Config:
        from_attributes = True


class OrderFilter(BaseModel):
    category: OrderCategory | None = None
    valid_since: datetime | None = None
    valid_until: datetime | None = None
    status: OrderStatus | None = None
    senior_id: int | None = None
    volunteer_id: int | None = None


class Order(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
