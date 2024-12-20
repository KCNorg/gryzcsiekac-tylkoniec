import os
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from src import crud, database, schemas
from src.models import OrderCategory, OrderStatus, UserSession
from src.schemas import CreateUserSession

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_phone_number(db, phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_user(db=db, user=user)


@app.put("/users/{user_id}", response_model=schemas.User)
def partial_update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_update=user_update, db_user=db_user)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


@app.post("/user-sessions", response_model=schemas.UserSession)
def create_user_session(
    user_session: CreateUserSession, db: Session = Depends(database.get_db)
) -> UserSession:
    return crud.create_user_session(db, user_session=user_session)


@app.get("/user-sessions", response_model=schemas.UserSession)
def get_user_session(token: str, db: Session = Depends(database.get_db)) -> UserSession:
    db_user_session = crud.get_user_session(db, token)
    if db_user_session is None:
        raise HTTPException(status_code=404, detail="User session not found")
    return db_user_session


@app.get("/orders")
def read_orders(
    category: OrderCategory = None,
    valid_since: datetime = None,
    valid_until: datetime = None,
    status: OrderStatus = None,
    senior_id: int = None,
    volunteer_id: int = None,
    sort_by: str = None,
    sort_direction: str = None,
    skip: int = 0,
    limit: int = 100,
    latitude: str = None,
    longitude: str = None,
    db: Session = Depends(database.get_db),
):
    orders = crud.get_orders(
        db,
        category=category,
        valid_since=valid_since,
        valid_until=valid_until,
        skip=skip,
        status=status,
        senior_id=senior_id,
        volunteer_id=volunteer_id,
        limit=limit,
        sort_by=sort_by,
        sort_direction=sort_direction,
        latitude=latitude,
        longitude=longitude,
    )
    return orders


@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(database.get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.put("/orders/{order_id}", response_model=schemas.Order)
def partial_update_order(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(database.get_db),
):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud.update_order(db=db, order_update=order_update, db_order=db_order)


@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(database.get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return db_order


@app.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    return crud.create_order(db=db, order=order)


@app.post("/register", response_model=schemas.User)
def register_user(
    request: schemas.RegisterRequest, db: Session = Depends(database.get_db)
):
    return crud.register_user(db=db, request=request)


@app.post("/login", response_model=schemas.User)
def login_user(request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    return crud.login_user(db=db, request=request)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
