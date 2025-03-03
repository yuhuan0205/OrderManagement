from sqlalchemy.orm import Session
from fastapi import Depends
from infrastructure.database.postgre_order_repository import PostgreOrderRepository
from core.order.order_repository import OrderRepository
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return PostgreOrderRepository(db)