from enum import Enum

class ShipmentStatus(Enum):
    PNEDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED = range(5)
