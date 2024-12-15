import os
import urllib.parse
from datetime import datetime
from typing import Dict

import requests
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
    valid_since: datetime | None = None
    valid_until: datetime | None = None
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


class RegisterRequest(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    address: str | None = None
    type: UserType
    image_url: str | None = None
    description: str | None = None
    token: str

    def get_geocode(self, address: str):
        base_url = "https://geocode.maps.co/search"
        api_key = os.getenv("GEOCODE_API_KEY")
        encoded_address = urllib.parse.quote(address)
        url = f"{base_url}?q={encoded_address}&api_key={api_key}"

        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def to_user_create(self) -> UserCreate:
        geo_data = self.get_geocode(self.address) if self.address else None

        return UserCreate(
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
            address=self.address,
            longitude=float(geo_data[0].get("lon")) if geo_data else None,
            latitude=float(geo_data[0].get("lat")) if geo_data else None,
            type=self.type,
            image_url=self.image_url,
            description=self.description,
        )

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    phone_number: str
    token: str

    class Config:
        from_attributes = True
