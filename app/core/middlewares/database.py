from dotenv import load_dotenv
from pymongo import MongoClient, TEXT
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

try:
    db.create_collection("products")
    print("products collection added")
    db.products.create_index([("name", TEXT)])
    print("index for products added")
    db.create_collection("users")
    print("users collection added")
    db.users.create_index([("username", TEXT)])
    db.users.create_index([("email", TEXT)])
    print("index for users added")

except Exception as e:
    if e == CollectionInvalid:
        pass
    else:
        print(e)

products_collection = db.products
users_collection = db.users
orders_collection = db.orders
carts_collection = db.carts
