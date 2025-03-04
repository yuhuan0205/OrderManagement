from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from api.dependencies.dependencies import get_order_repository
from api.order_adapters.self_platform_order_adapter import SelfPlatformCreateOrderAdapter, CreateOrderRequest, SelfPlatformUpdateOrderAdapter, UpdateOrderRequest
from core.order.order_repository import OrderRepository

router = APIRouter(
    prefix="/orders",
    tags=["otders"],
    responses={404:{"description": "Not found"}}
)

@router.get("/{order_id}")
async def get_order(order_id: UUID, order_repo: OrderRepository = Depends(get_order_repository)):
    order = order_repo.get(order_id)
    if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/")
async def create_order(request: CreateOrderRequest, order_repo: OrderRepository = Depends(get_order_repository)):
    try:
        order = SelfPlatformCreateOrderAdapter(request)
        order_repo.create(order)
        return {"order_id": order.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/")
async def update_order(request: UpdateOrderRequest, order_repo: OrderRepository = Depends(get_order_repository)):
    try:
        order = SelfPlatformUpdateOrderAdapter(request)
        order_repo.update(order)
        return {"order_id": order.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{order_id}")
async def delete_order(order_id: UUID, order_repo: OrderRepository = Depends(get_order_repository)):
    order_repo.delete(order_id)