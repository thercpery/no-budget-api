from fastapi import security, Depends
import email_validator
from passlib.hash import bcrypt
from dotenv import load_dotenv
import jwt
import os

from ..middlewares import database
from ..models.User import LoginUser

load_dotenv()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
oauth2schema = security.OAuth2PasswordBearer("/api/users/login")

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


async def create_token(user: dict):
    del user["orders"]
    del user["mobileNo"]
    del user["address"]
    del user["dateCreated"]
    del user["dateUpdated"]

    token = jwt.encode(user, JWT_SECRET_KEY)
    return dict(access_token=token, token_type="bearer")


async def get_current_user(token: str = Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user = users_collection.find_one({"_id": payload["id"]})
    except Exception as e:
        return False

    return user


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


async def login_user(user_data: LoginUser):
    db_user = await get_user_by_username(username=user_data.username)

    if not db_user:
        return False

    is_password_correct = bcrypt.verify(user_data.password, db_user["password"])
    if not is_password_correct:
        return False

    return await create_token(user=db_user)
