from datetime import datetime
from enum import Enum
from typing import List, Dict

from pydantic import BaseModel

from src.models import UserType, OrderCategory, OrderStatus


class UserBase(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    address: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    type: str
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

class OrderBase(BaseModel):
    category: OrderCategory
    description: Dict = {}
    valid_since: datetime
    valid_until: datetime
    status: OrderStatus = OrderStatus.PENDING
    senior_id: int
    volunteer_id: int = None

    class Config:
        orm_mode = True

class GetOrdersRequest(BaseModel):
    ids: List[int]

class GetOrdersResponse(BaseModel):
    orders: List[OrderBase]

    class Config:
        orm_mode = True


class Order(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
