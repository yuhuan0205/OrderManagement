from abc import ABC, abstractmethod
from core.order.order import OrderBase
import uuid

class OrderRepository(ABC):
    @abstractmethod
    def get(id: uuid.UUID) -> OrderBase:
        raise NotImplementedError()
    
    @abstractmethod
    def create(order: OrderBase) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def update(order: OrderBase) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def delete(order_id: uuid.UUID) -> None:
        raise NotImplementedError()