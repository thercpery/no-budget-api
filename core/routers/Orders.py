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


@router.post("/checkout/cart", response_description="Checkout select items from current user's cart", response_model=Order)
async def checkout_from_cart(
        current_user: dict = Depends(Users.get_current_user),
        product_ids: CheckoutFromCart = Body()
):
    if current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    is_order_created = await Orders.checkout_from_cart(
        product_ids=product_ids.product_ids,
        username=current_user["username"]
    )

    if not is_order_created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One of your cart items is either not existing in our database, is not in your cart, "
                   "or your cart is empty. Please try again."
        )

    return is_order_created


@router.post("/checkout/cart/all", response_description="Checkout all items from the cart", response_model=Order)
async def checkout_all_items_in_cart(
        current_user: dict = Depends(Users.get_current_user)
):
    if current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    is_order_created = await Orders.checkout_all_items_in_cart(
        username=current_user["username"]
    )

    if not is_order_created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty. Please fill it up first."
        )

    return is_order_created

