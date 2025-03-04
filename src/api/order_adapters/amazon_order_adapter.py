import uuid
from core.order.order import OrderBase, Shipment, OrderItem
from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime

class AmazonOrderAdapter(OrderBase):
    def __init__(self, adaptee: "AmazonOrder"):
        self.__adaptee = adaptee
        self.__id = uuid.uuid4()
    
    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def shipments(self) -> list[Shipment]:
        return [
        Shipment(
            self.__adaptee.delivery.address,
            [OrderItem(order_item.name, order_item.price, order_item.quantity) for order_item in self.__adaptee.delivery.order_items]
        )
        ]


class AmazonOrder(BaseModel):
    delivery: "AmazonDelivery" 

class AmazonDelivery(BaseModel):
    address: str  
    items: list["AmazonOrderProduct"]
    delivery_time: datetime

class AmazonOrderProduct(BaseModel):
    name: str
    cost: Decimal
    quantity: int