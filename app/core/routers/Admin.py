from fastapi import APIRouter, Body, HTTPException, status, Depends
from typing import List

from ..models.User import LoginUser, UserDisplay, UserGrantOrRevokeAdminAccess
from ..models.Product import ProductBase, ProductUpdate
from ..models.Order import Order
from ..services import Users, Admin

router = APIRouter()


@router.post("/login", response_description="Login users with admin access")
async def login_admin_users(user_data: LoginUser):
    pass


@router.get("/users", response_description="Get all users data", response_model=List[UserDisplay])
async def get_all_users(current_user: dict = Depends(Users.get_current_user)):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )


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


@router.get("/products", response_description="Get all products", response_model=List[ProductBase])
async def get_all_products(current_user: dict = Depends(Users.get_current_user)):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )


@router.post("/products", response_description="Add a product", response_model=ProductBase)
async def add_product(
        current_user: dict = Depends(Users.get_current_user),
        product_data: ProductBase = Body()
):
    pass


@router.patch("/products/update/{_id}", response_description="Update products", response_model=ProductBase)
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


@router.get("/orders", response_description="Get all orders", response_model=List[Order])
async def get_all_orders(current_user: dict = Depends(Users.get_current_user)):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint. Please contact your administrator."
        )
