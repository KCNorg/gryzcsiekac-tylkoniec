from pydantic import BaseModel

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