import uuid
from core.order.shipment import ShipmentStatus
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, default=uuid.uuid4)
    buyer_id = Column(UUID(as_uuid=True), nullable=False)

    shipments = relationship("Shipment", backref="order", cascade="all, delete-orphan")

class Shipment(Base):
    __tablename__ = "shipments"

    order_id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    id = Column(UUID(as_uuid=True), primary_key=True)
    shipment_status = Column(SQLEnum(ShipmentStatus), nullable=False)
    destination = Column(String, nullable=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    shipment_id = Column(UUID(as_uuid=True), primary_key=True)
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # 使用 Decimal 儲存金額
    quantity = Column(Integer, nullable=False)

