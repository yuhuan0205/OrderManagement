from abc import ABC, abstractmethod
from order import Order
import uuid

class OrderRepository(ABC):
    @abstractmethod
    def get(id: uuid.UUID) -> Order:
        pass
    
    @abstractmethod
    def save(order: Order) -> None:
        pass