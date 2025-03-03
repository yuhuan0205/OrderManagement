import uuid
from order_item import OrderItem
from enum import Enum

class Shipment:
    def __init__(self, destination: str, order_items: list[OrderItem], id: uuid.UUID = uuid.uuid4(), shipment_status: "ShipmentStatus" = "ShipmentStatus".PNEDING) -> None:
        self.id = id
        self.shipment_status = shipment_status
        self.destination = destination
        self.order_items = order_items


class ShipmentStatus(Enum):
    PNEDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED = range(5)