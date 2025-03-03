import uuid
from shipment import Shipment

class Order:
    def __init__(self, shipments: list[Shipment], buyer_id: uuid.UUID, id: uuid.UUID = uuid.uuid4()) -> None:
        self.id = id
        self.shipments = shipments
        self.buyer_id = buyer_id