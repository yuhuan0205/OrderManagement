from decimal import Decimal
from enum import Enum
import uuid
from abc import ABC, abstractmethod

class OrderBase(ABC):
    @property
    @abstractmethod
    def id(self) -> uuid.UUID:
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def shipments(self) -> list["Shipment"]:
        raise NotImplementedError()

class Order(OrderBase):
    def __init__(self, id: uuid.UUID, shipments: list["shipments"]):
        self.__id = id
        self.__shipments = shipments
    
    @property
    def id(self) -> uuid.UUID:
        return self.__id
    
    @property
    def shipments(self) -> list["Shipment"]:
        return self.__shipments


class ShipmentStatus(Enum):
    PNEDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED = range(5)

class Shipment:
    def __init__(self, destination: str, order_items: list["OrderItem"], id: uuid.UUID = None, shipment_status: "ShipmentStatus" = ShipmentStatus.PNEDING) -> None:
        if id is None:
            self.id = uuid.uuid4()
        else:
            self.id = id
        self.shipment_status = shipment_status
        self.destination = destination
        self.order_items = order_items

class OrderItem:
    def __init__(self, name: str, price: Decimal, quantity: int, id: uuid.UUID = None) -> None:
        if id is None:
            self.id = uuid.uuid4()
        else:
            self.id = id
        self.name = name
        self.price = self.__check_price(price)
        self.quantity = self.__check_quantity(quantity)

    def __check_price(self, price: Decimal) -> Decimal:
        """檢查價格是否為正數"""
        if price < 0:
            raise ValueError("價格不能為負")
        return price

    def __check_quantity(self, quantity: int) -> int:
        """檢查數量是否為正數"""
        if quantity <= 0:
            raise ValueError("數量不能小於等於0")
        return quantity