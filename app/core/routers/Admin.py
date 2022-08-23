from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from typing import List

from ..models.User import LoginUser, UserDisplay, UserGrantOrRevokeAdminAccess
from ..models.Product import ProductBase, ProductUpdate
from ..models.Order import Order
from ..services import Users, Admin

router = APIRouter()


@router.post("/login", response_description="Login users with admin access")
async def login_admin_users(user_data: LoginUser):
    token = await Admin.login_user(user_data=user_data)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials or user is not an admin"
        )

    return token


@router.get("/users", response_description="Get all users data", response_model=List[UserDisplay])
async def get_all_users(current_user: dict = Depends(Users.get_current_user)):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    return await Admin.get_all_users()


@router.patch("/grant-admin", response_description="Grant admin access to user")
async def grant_admin_access(
        current_user: dict = Depends(Users.get_current_user),
        username: UserGrantOrRevokeAdminAccess = Body()
):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    is_user_granted = await Admin.grant_admin_access(current_user=current_user, username=username.username)

    if not is_user_granted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is something wrong with your request. Try different credentials")

    return {
        "detail": f"{username.username} is now an admin."
    }


@router.patch("/revoke-admin", response_description="Revoke admin access to user")
async def revoke_admin_access(
        current_user: dict = Depends(Users.get_current_user),
        username: UserGrantOrRevokeAdminAccess = Body()
):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    is_user_revoked = await Admin.revoke_admin_access(current_user=current_user, username=username.username)

    if not is_user_revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is something wrong with your request. Try different credentials")

    return {
        "detail": f"{username.username} has now his / her admin access revoked."
    }


@router.get("/products", response_description="Get all products", response_model=List[ProductBase])
async def get_all_products(current_user: dict = Depends(Users.get_current_user)):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    return await Admin.get_all_products()


@router.post("/products", response_description="Add a product", response_model=ProductBase)
async def add_product(
        current_user: dict = Depends(Users.get_current_user),
        product_data: ProductBase = Body()
):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    product = jsonable_encoder(product_data)
    return await Admin.add_products(product_data=product)


@router.patch("/products/{_id}", response_description="Update products", response_model=ProductBase)
async def update_product(
        _id: str,
        product_data: ProductUpdate = Body(),
        current_user: dict = Depends(Users.get_current_user)
):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    is_item_updated = await Admin.update_product(_id=_id, product_data=product_data)
    if not is_item_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not in our database or not in stock")

    return is_item_updated


@router.patch("/products/shelf-or-resell/{_id}", response_description="Shelf or resell product")
async def shelf_or_resell_product(
        _id: str,
        current_user: dict = Depends(Users.get_current_user)
):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    is_product_shelved_or_resold = await Admin.shelf_or_resell_product(_id=_id)
    if not is_product_shelved_or_resold:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not in our database or not in stock")

    return is_product_shelved_or_resold


@router.get("/orders", response_description="Get all orders", response_model=List[Order])
async def get_all_orders(current_user: dict = Depends(Users.get_current_user)):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )

    return await Admin.get_all_orders()
