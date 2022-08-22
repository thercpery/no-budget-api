from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from typing import List

from ..models.User import \
    UserBase, UserChangePassword, LoginUser, UserDisplay, UserGrantOrRevokeAdminAccess, UserChangeUsername
from ..services import Users

router = APIRouter()


@router.post("/register", response_description="Register a user")
async def register_user(user_data: UserBase = Body()):
    user_data = jsonable_encoder(user_data)
    is_user_registered = await Users.register_user(user_data=user_data)

    if not is_user_registered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is something wrong with your registration. Please try again")

    return is_user_registered


@router.post("/login", response_description="Login user")
async def login_user(user_data: LoginUser):
    token = await Users.login_user(user_data=user_data)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

    return token


@router.get("/me", response_description="Get current user", response_model=UserDisplay)
async def get_current_user(current_user: dict = Depends(Users.get_current_user)):
    return await Users.get_user_by_username(username=current_user["username"])


@router.get("/", response_description="Get all users", response_model=List[UserDisplay])
async def get_all_users(current_user: dict = Depends(Users.get_current_user)):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not authorized to access this endpoint. Please contact your administrator.")

    return await Users.get_all_users()


@router.patch("/change-password", response_description="Change user's password")
async def change_password(
        current_user: dict = Depends(Users.get_current_user),
        new_password_data: UserChangePassword = Body()):
    is_password_changed = await Users.is_password_changed(user=current_user, new_password_data=new_password_data)

    if not is_password_changed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is something wrong with your password. Please try again")

    return {
        "detail": "Changed password successfully. Please log in again."
    }


@router.patch("/grant-admin", response_description="Grant or revoke admin access to user")
async def grant_admin_access(
        current_user: dict = Depends(Users.get_current_user),
        username: UserGrantOrRevokeAdminAccess = Body()):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed")

    is_user_granted = await Users.grant_admin_access(current_user=current_user, username=username.username)

    if not is_user_granted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is something wrong with your request. Try different credentials")

    return {
        "detail": f"{username.username} is now an admin."
    }


@router.patch("/revoke-admin", response_description="Grant or revoke admin access to user")
async def revoke_admin_access(
        current_user: dict = Depends(Users.get_current_user),
        username: UserGrantOrRevokeAdminAccess = Body()):
    if not current_user["isAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed")

    is_user_granted = await Users.revoke_admin_access(current_user=current_user, username=username.username)

    if not is_user_granted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is something wrong with your request. Try different credentials")

    return {
        "detail": f"{username.username} has now his / her admin access revoked."
    }


@router.patch("/change-username", response_description="Change current user's username", response_model=UserDisplay)
async def change_username(
        current_user: dict = Depends(Users.get_current_user),
        new_username: UserChangeUsername = Body()
):
    is_user_updated = await Users.change_username(current_user=current_user, new_username=new_username.username)

    if not is_user_updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There's something wrong with your credentials. Try different ones.")

    return is_user_updated

