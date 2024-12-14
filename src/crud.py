from typing import Type, Optional

from sqlalchemy.orm import Session
from src.models import User
from src.schemas import UserCreate, UserUpdate


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

def update_user(db: Session, user_update: UserUpdate, db_user: Type[User]) -> Type[User]:
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user