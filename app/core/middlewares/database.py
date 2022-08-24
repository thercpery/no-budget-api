from dotenv import load_dotenv
from pymongo import MongoClient, TEXT, database
from pymongo.errors import CollectionInvalid
import os

load_dotenv()

DB_ENV = os.environ.get("DB_ENV")
if DB_ENV == "local":
    MONGODB_URI = "mongodb://localhost:27017"

else:
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")

    MONGODB_URI = f"mongodb+srv://{DB_USER}:{DB_PASS}@wdc028-course-booking.dwfxo.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)
db = client["no_budget"]


def create_products_collection(db: database):
    try:
        db.create_collection("products")
        print("products collection added")
    except Exception as e:
        if type(e) == CollectionInvalid:
            pass
        else:
            print(e)


def create_users_collection(db: database):
    try:
        db.create_collection("users")
        print("users collection added")
    except Exception as e:
        if type(e) == CollectionInvalid:
            pass
        else:
            print(e)


def create_carts_collection(db: database):
    try:
        db.create_collection("carts")
        print("carts collection added")
    except Exception as e:
        if type(e) == CollectionInvalid:
            pass
        else:
            print(e)


def create_orders_collection(db: database):
    try:
        db.create_collection("orders")
        print("orders collection added")
    except Exception as e:
        if type(e) == CollectionInvalid:
            pass
        else:
            print(e)


create_products_collection(db)
create_users_collection(db)
create_carts_collection(db)
create_orders_collection(db)

db.products.create_index([("name", TEXT)])
db.users.create_index([("username", TEXT), ("email", TEXT)])
db.carts.create_index([("userId", TEXT)])

products_collection = db.products
users_collection = db.users
carts_collection = db.carts
orders_collection = db.orders
