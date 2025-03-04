import uuid
from core.order.order import OrderBase, Shipment, OrderItem
from decimal import Decimal
from pydantic import BaseModel

class SelfPlatformOrderAdapter(OrderBase):
    def __init__(self, adaptee: "CreateOrderRequest"):
        self.__adaptee = adaptee
        self.__id = uuid.uuid4()
    
    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def shipments(self) -> list[Shipment]:
        return [
        Shipment(
            shipment.destination,
            [OrderItem(order_item.name, order_item.price, order_item.quantity) for order_item in shipment.order_items]
        )
        for shipment in self.__adaptee.shipments
        ]


class CreateOrderRequest(BaseModel):
    shipments: list["CreateShipmentRequest"]

class CreateShipmentRequest(BaseModel):
    destination: str
    order_items: list["CreateOrderItemReuqest"]

class CreateOrderItemReuqest(BaseModel):
    name: str
    price: Decimal
    quantity: int