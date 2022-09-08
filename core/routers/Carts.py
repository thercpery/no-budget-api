from fastapi import APIRouter, HTTPException, status, Depends, Body

from ..models.Cart import CartItems, AddToCart, RemoveToCart
from ..services import Carts
from ..services import Users

router = APIRouter()


@router.get("/",
            response_description="Get cart items from current user",
            response_model=CartItems)
async def get_cart_from_user(current_user: dict = Depends(Users.get_current_user)):
    if current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator.")

    return await Carts.get_cart_from_user(user_id=current_user["_id"])


@router.post("/",
             response_description="Add product to cart",
             response_model=CartItems
)
async def add_product_to_cart(
        current_user: dict = Depends(Users.get_current_user),
        product: AddToCart = Body()
):
    if current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator.")

    if product.quantity == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product quantity not allowed."
        )

    product_id = product.product_id
    is_product_added = await Carts.add_product_to_cart(
        product_id=product_id,
        quantity=product.quantity,
        user_id=current_user["_id"])
    if not is_product_added:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not found in the database or is not in stock."
        )

    return is_product_added


@router.patch("/remove", response_description="Remove one item from cart")
async def remove_items_from_cart(
        current_user: dict = Depends(Users.get_current_user),
        product_ids: RemoveToCart = Body()
):
    if current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator.")

    is_item_removed = await Carts.remove_items_from_cart(product_ids=product_ids, user_id=current_user["_id"])

    if not is_item_removed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty. Please fill it up first"
        )

    return is_item_removed

