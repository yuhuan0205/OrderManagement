import uuid
from core.order.order import OrderBase, Shipment, OrderItem
from decimal import Decimal
from pydantic import BaseModel

class HKTVmallOrderAdapter(OrderBase):
    def __init__(self, adaptee: "HKTVmallOrder"):
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

class HKTVmallOrder(BaseModel):
    shipments: list["HKTVmallShipment"]
    order_number: str

class HKTVmallShipment(BaseModel):
    destination: str
    order_items: list["HKTVmallOrderItem"]
    estimated_arrival: str

class HKTVmallOrderItem(BaseModel):
    name: str
    price: Decimal
    quantity: int
    product_code: str 

