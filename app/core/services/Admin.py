from fastapi import security
from passlib.hash import bcrypt
from dotenv import load_dotenv
from datetime import datetime
import os

from ..middlewares import database
from ..models.User import LoginUser
from ..models.Product import ProductBase, ProductUpdate, RestockProduct
from ..models.Order import Order
from ..services import Users, Products

load_dotenv()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
oauth2schema = security.OAuth2PasswordBearer("/api/admin/login")

users_collection = database.users_collection
products_collection = database.products_collection
orders_collection = database.orders_collection


async def login_user(user_data: LoginUser):
    db_user = await Users.get_user_by_username(username=user_data.username)

    if not db_user or not db_user["isAdmin"]:
        return False

    is_password_correct = bcrypt.verify(user_data.password, db_user["password"])
    if not is_password_correct:
        return False

    return await Users.create_token(user=db_user)


async def get_all_users():
    users = list(users_collection.find({}, {"password": 0}))

    return users


async def grant_admin_access(current_user: dict, username: str) -> bool:
    db_user = await Users.get_user_by_username(username=username)

    if db_user is None:
        return False

    if db_user["username"] == current_user["username"]:
        return False

    db_user["isAdmin"] = True
    db_user["dateUpdated"] = datetime.now()

    users_collection.update_one({"_id": db_user["_id"]}, {"$set": db_user})
    return True


async def revoke_admin_access(current_user: dict, username: str) -> bool:
    db_user = await Users.get_user_by_username(username=username)

    if db_user is None:
        return False

    if db_user["username"] == current_user["username"]:
        return False

    db_user["isAdmin"] = False
    db_user["dateUpdated"] = datetime.now()

    users_collection.update_one({"_id": db_user["_id"]}, {"$set": db_user})
    return True


async def add_products(product_data: dict):
    new_product = products_collection.insert_one(product_data)
    created_product = products_collection.find_one({"_id": new_product.inserted_id})

    return created_product


async def get_all_products():
    return list(products_collection.find({}))


async def update_product(_id: str, product_data: ProductUpdate):
    product = await Products.get_product_by_id(_id=_id)
    if product is None:
        return False

    product["name"] = product_data.name
    product["description"] = product_data.description
    product["categories"] = product_data.categories
    product["sku"] = product_data.sku
    product["quantity"] = product_data.quantity
    product["price"] = product_data.price
    product["dateUpdated"] = datetime.now()

    products_collection.update_one({"_id": _id}, {"$set": product})
    return await Products.get_product_by_id(_id=_id)


async def shelf_or_resell_product(_id: str):
    product = await Products.get_product_by_id(_id=_id)
    if product is None:
        return False

    product["isAvailable"] = not product["isAvailable"]
    product["dateUpdated"] = datetime.now()
    products_collection.update_one({"_id": _id}, {"$set": product})
    return await Products.get_product_by_id(_id=_id)


async def get_all_orders():
    return list(orders_collection.find({}))
