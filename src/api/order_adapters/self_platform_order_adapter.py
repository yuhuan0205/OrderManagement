import uuid
from core.order.order import OrderBase, Shipment, OrderItem, ShipmentStatus
from decimal import Decimal
from pydantic import BaseModel

class SelfPlatformCreateOrderAdapter(OrderBase):
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

class SelfPlatformUpdateOrderAdapter(OrderBase):
    def __init__(self, adaptee: "UpdateOrderRequest"):
        self.__adaptee = adaptee
        self.__id = adaptee.id
    
    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def shipments(self) -> list[Shipment]:
        return [
        Shipment(
            shipment.destination,
            [OrderItem(order_item.name, order_item.price, order_item.quantity, order_item.id) for order_item in shipment.order_items],
            shipment_status = shipment.shipment_status,
            id=shipment.id
        )
        for shipment in self.__adaptee.shipments
        ]

class UpdateOrderRequest(BaseModel):
    id: uuid.UUID
    shipments: list["UpdateShipmentRequest"]

class UpdateShipmentRequest(BaseModel):
    id: uuid.UUID
    destination: str
    order_items: list["UpdateOrderItemReuqest"]
    shipment_status: ShipmentStatus

class UpdateOrderItemReuqest(BaseModel):
    id: uuid.UUID
    name: str
    price: Decimal
    quantity: int