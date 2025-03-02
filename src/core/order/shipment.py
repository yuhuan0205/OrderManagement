from order_item import OrderItem
from shipment_status import ShipmentStatus
import uuid

class Shipment:
    def __init__(self, id: uuid.UUID, shipment_status: ShipmentStatus ,order_items: list[OrderItem]) -> None:
        
        pass