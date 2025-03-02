from decimal import Decimal
import uuid

class OrderItem:
    def __init__(self, id: uuid.UUID, name: str, price: Decimal, quantity: int) -> None:
        self.id = id
        self.name = name
        self.price = self.__check_price(price)
        self.quantity = self.__check_quantity(quantity)
    
    @classmethod
    def create(cls, name: str, price: Decimal, quantity: int) -> "OrderItem":
        """建立訂單項目"""
        id = uuid.uuid4()
        return cls(id, name, price, quantity)

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