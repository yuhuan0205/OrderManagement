from decimal import Decimal
import uuid
from pydantic import BaseModel

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