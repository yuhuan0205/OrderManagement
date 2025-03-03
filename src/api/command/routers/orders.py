import uuid
from fastapi import APIRouter, Depends
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel
from dependencies.dependencies import get_order_repository

router = APIRouter(
    prefix="/orders",
    tags=["otders"],
    responses={404:{"description": "Not found"}}
)

order_repo = Depends(get_order_repository)

@router.get("/")
async def get_orders():
    pass

@router.get("/{order_id}")
async def get_order(order_id: UUID):
    pass

@router.post("/")
async def create_order(request: "CreateOrderRequest"):

    return 



class CreateOrderRequest(BaseModel):
    buyer_id: uuid.UUID
    shipments: list["CreateShipmentRequest"]

class CreateShipmentRequest(BaseModel):
    destination: str
    order_items: list["CreateOrderItemReuqest"]

class CreateOrderItemReuqest(BaseModel):
    name: str
    price: Decimal
    quantity: int