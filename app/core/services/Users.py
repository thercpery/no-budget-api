import email_validator
from passlib.hash import bcrypt
from dotenv import load_dotenv
import os

from ..middlewares import database
from ..models.User import UserBase

load_dotenv()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

users_collection = database.users_collection


async def get_user_by_username(username: str):
    return users_collection.find_one({"username": username})


async def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})


async def verify_duplicates(username: str, email: str) -> bool:
    db_username = await get_user_by_username(username=username)
    db_email = await get_user_by_email(email=email)

    if (db_username is not None) or (db_email is not None):
        return True

    return False


def check_email_if_valid(email: str) -> bool:
    try:
        email_validator.validate_email(email)
        return True
    except email_validator.EmailSyntaxError:
        return False


async def register_user(user_data: dict):
    is_email_valid = check_email_if_valid(user_data["email"])
    if not is_email_valid:
        return False

    is_there_duplicates = await verify_duplicates(
        username=user_data["username"],
        email=user_data["email"])

    if is_there_duplicates:
        return False

    user_data["password"] = bcrypt.hash(user_data["password"])

    new_user = users_collection.insert_one(user_data)
    user_obj = users_collection.find_one({"_id": new_user.inserted_id})
    del user_obj["password"]

    return user_obj


