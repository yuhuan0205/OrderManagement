import uuid
from core.order.order_repository import OrderRepository
from core.order.order import OrderBase, Order, OrderItem, Shipment
from infrastructure.database.models import Order as ORMOrder, Shipment as ORMShipment, OrderItem as ORMOrderItem
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.dialects.postgresql import insert

class PostgreOrderRepository(OrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: uuid.UUID) -> OrderBase:
        result = self.db.execute(
            select(ORMOrder)
            .options(
                joinedload(ORMOrder.shipments).joinedload(ORMShipment.order_items)
            )
            .filter(ORMOrder.id == id)
        )
        order = result.scalars().first()
        if order == None:
            return None
        return self._to_domain_model(order)

    def create(self, order: OrderBase) -> None:
        print(order.shipments)
        insert_stmt = insert(ORMOrder).values(
            id=order.id
        )
        self.db.execute(insert_stmt)
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
    
    def update(self, order: OrderBase) -> None:
        for shipment in order.shipments:
            stmt = (
                update(ORMShipment)
                .where(ORMShipment.id == shipment.id)
                .values(
                    shipment_status=shipment.shipment_status,
                    destination=shipment.destination,
                )
            )
            self.db.execute(stmt)

            for item in shipment.order_items:
                item_stmt = (
                    update(ORMOrderItem)
                    .where(ORMOrderItem.id == item.id)
                    .values(
                        name=item.name,
                        price=item.price,
                        quantity=item.quantity,
                    )
                )
                self.db.execute(item_stmt)

        self.db.commit()

    def delete(self, id: uuid.UUID) -> None:
        stmt = delete(ORMOrder).where(ORMOrder.id == id)
        self.db.execute(stmt)
        self.db.commit()

    def _to_domain_model(self, orm_order: ORMOrder) -> OrderBase:
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
        return Order(id=orm_order.id, shipments=shipments)