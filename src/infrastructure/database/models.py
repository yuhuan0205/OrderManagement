import uuid
from core.order.order import ShipmentStatus
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipments = relationship("Shipment", back_populates="order")

class Shipment(Base):
    __tablename__ = "shipments"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True)
    shipment_status = Column(SQLEnum(ShipmentStatus), nullable=False)
    destination = Column(String, nullable=False)

    order = relationship("Order", back_populates="shipments")
    order_items = relationship("OrderItem", back_populates="shipment")

class OrderItem(Base):
    __tablename__ = "order_items"
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False, primary_key=True
                         )
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)

    shipment = relationship("Shipment", back_populates="order_items")
