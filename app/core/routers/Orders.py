from fastapi import APIRouter, HTTPException, status, Body, Depends
from typing import List

from ..models.Order import Order, OrderOneProduct, CheckoutFromCart
from ..services import Orders, Users

router = APIRouter()


@router.get("/", response_description="Get orders of current user", response_model=List[Order])
async def get_orders_from_user(current_user: dict = Depends(Users.get_current_user)):
    if current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )
    return await Orders.get_orders_from_user(user_id=current_user["_id"])


@router.post("/checkout", response_description="Order one product directly", response_model=Order)
async def order_now(
        current_user: dict = Depends(Users.get_current_user),
        product_data: OrderOneProduct = Body()
):
    if current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    is_order_created = await Orders.order_now(product_data=product_data, username=current_user["username"])

    if not is_order_created:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product does not exist"
        )

    return is_order_created
