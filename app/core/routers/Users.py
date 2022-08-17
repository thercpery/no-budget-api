from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ..models.User import UserBase, UserChangePassword, LoginUser
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
