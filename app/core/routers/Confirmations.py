from fastapi import APIRouter, Depends, HTTPException, status
from ..services import Confirmations

router = APIRouter()


@router.get("/{_id}", response_description="Confirm a user thru its email")
async def confirm_user(_id: str):
    is_user_confirmed = await Confirmations.confirm_user(_id=_id)

    if not is_user_confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The confirmation link has been expired or does not exist.")

    return {
        "detail": "Successfully confirmed!"
    }
