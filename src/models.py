import enum

from sqlalchemy import (JSON, TIMESTAMP, Column, Enum, Float, ForeignKey,
                        Integer, String)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserType(enum.Enum):
    SENIOR = "senior"
    VOLUNTEER = "volunteer"


class OrderStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    type = Column(Enum(UserType), nullable=False)
    image_url = Column(String, nullable=True)
    description = Column(String, nullable=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum(UserType), nullable=False)
    description = Column(JSON, nullable=False, default={})
    created_at = Column(TIMESTAMP, nullable=False)
    valid_since = Column(TIMESTAMP, nullable=False)
    valid_until = Column(TIMESTAMP, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    senior_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    volunteer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
