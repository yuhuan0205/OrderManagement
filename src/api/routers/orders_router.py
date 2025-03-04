from fastapi import APIRouter, Depends
from uuid import UUID
from api.dependencies.dependencies import get_order_repository
from api.order_adapters.self_platform_order_adapter import SelfPlatformOrderAdapter, CreateOrderRequest
from core.order.order_repository import OrderRepository

router = APIRouter(
    prefix="/orders",
    tags=["otders"],
    responses={404:{"description": "Not found"}}
)

@router.get("/")
async def get_orders():
    pass

@router.get("/{order_id}")
async def get_order(order_id: UUID, order_repo: OrderRepository = Depends(get_order_repository)):
    order = order_repo.get(order_id)
    return order

@router.post("/")
async def create_order(request: CreateOrderRequest, order_repo: OrderRepository = Depends(get_order_repository)):
    order = SelfPlatformOrderAdapter(request)
    order_repo.create(order)
    return order.id

@router.delete("/{order_id}")
async def delete_order(order_id: UUID, order_repo: OrderRepository = Depends(get_order_repository)):
    order_repo.delete(order_id)
    return