import uuid
from core.order.order_repository import OrderRepository
from core.order.order import Order
from core.order.shipment import Shipment
from core.order.order_item import OrderItem
from models import Order as ORMOrder, Shipment as ORMShipment, OrderItem as ORMOrderItem
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

class PostgreOrderRepository(OrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: uuid.UUID) -> Order:
        """根據 id 取得 Order，並轉換為領域模型"""
        orm_order = self.db.query(ORMOrder).filter(ORMOrder.id == id).first()
        if not orm_order:
            return None

        # 轉換 ORM 物件為領域模型
        return self._to_domain_model(orm_order)

    def save(self, order: Order) -> None:
        """使用 UPSERT (INSERT ... ON CONFLICT) 來保存訂單"""
        upsert_stmt = insert(ORMOrder).values(
            id=order.id
        ).on_conflict_do_update(
            index_elements=["id"],
            set_=
        )
        self.db.execute(upsert_stmt)

        # 先刪除舊的 Shipment，再新增
        self.db.query(ORMShipment).filter(ORMShipment.order_id == order.id).delete()

        for shipment in order.shipments:
            new_shipment = ORMShipment(
                id=shipment.id,
                shipment_status=shipment.shipment_status,
                destination=shipment.destination,
                order_id=order.id
            )
            self.db.add(new_shipment)

            for item in shipment.order_items:
                new_item = ORMOrderItem(
                    id=item.id,
                    name=item.name,
                    price=item.price,
                    quantity=item.quantity,
                    shipment_id=shipment.id
                )
                self.db.add(new_item)

        self.db.commit()
    
    def _to_domain_model(self, orm_order: ORMOrder) -> Order:
        """將 ORM 物件轉換為領域模型"""
        shipments = [
            Shipment(
                id=shipment.id,
                shipment_status=shipment.shipment_status,
                destination=shipment.destination,
                order_items=[
                    OrderItem(
                        id=item.id,
                        name=item.name,
                        price=item.price,
                        quantity=item.quantity
                    )
                    for item in shipment.order_items
                ]
            )
            for shipment in orm_order.shipments
        ]
        return Order(id=orm_order.id, shipments=shipments, buyer_id=orm_order.buyer_id)