from fastapi import APIRouter, HTTPException, status, Depends, Body

from ..models.Cart import CartItems, AddToCart
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

    product_id = product.product_id
    is_product_added = await Carts.add_product_to_cart(product_id=product_id, user_id=current_user["_id"])
    if not is_product_added:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not found in the database."
        )

    return is_product_added