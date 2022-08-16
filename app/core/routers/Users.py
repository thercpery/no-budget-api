from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ..models.User import UserBase, UserChangePassword
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
