from fastapi.encoders import jsonable_encoder
from datetime import datetime
from ..middlewares import database
from ..models.Order import OrderOneProduct, Order
from ..services import Users, Products

orders_collection = database.orders_collection
carts_collection = database.carts_collection
users_collection = database.users_collection
products_collection = database.products_collection


async def get_orders_from_user(user_id: str):
    return list(orders_collection.find({"userId": user_id}))


async def order_now(
        product_data: OrderOneProduct,
        username: str
):
    # Get current user from db
    current_user = await Users.get_user_by_username(username=username)

    # Create the products array
    products = []

    # Get product data from the database from the user input
    db_product = await Products.get_product_by_id(_id=product_data.product_id)

    # If no product found, return false
    if db_product is None:
        return False

    # Copy db_product to product_copy
    product_copy = db_product.copy()

    # Delete unnecessary data from product_copy
    del product_copy["description"]
    del product_copy["categories"]
    del product_copy["isAvailable"]
    del product_copy["dateCreated"]
    del product_copy["dateUpdated"]

    # Change db_product["price"] to db_product["price"] * quantity and db_product["quantity] to product_data.quantity
    product_copy["quantity"] = product_data.quantity
    product_copy["price"] = product_copy["price"] * product_data.quantity

    # Append product from db into the products array
    products.append(product_copy)

    # Compute total price by product price * quantity
    total_price = product_copy["price"] * product_data.quantity

    # Gather the user ID and product from DB into a "data" variable
    data = {
        "userId": current_user["_id"],
        "products": products,
        "totalPrice": total_price
    }

    # Store them inside the Order model
    order_obj = Order(
        userId=data["userId"],
        products=data["products"],
        totalPrice=data["totalPrice"]
    )

    current_time = datetime.now()

    # Put the model object into a jsonable_encoder function
    order_data = jsonable_encoder(order_obj)

    # Create order document
    new_order = orders_collection.insert_one(order_data)

    # Get newly-created order
    new_order_obj = orders_collection.find_one({"_id": new_order.inserted_id})

    # Deduct product's quantity by the product_data.quantity
    db_product["quantity"] = db_product["quantity"] - product_data.quantity

    # If db_product's quantity reaches zero, make product["isAvailable"] to false
    if db_product["quantity"] == 0:
        db_product["isAvailable"] = False

    # Update product in the database
    db_product["dateUpdated"] = current_time
    products_collection.update_one({"_id": db_product["_id"]}, {"$set": db_product})

    # Add the new order to the user document
    current_user["orders"].append(new_order_obj)

    # Update user document
    current_user["date"] = current_time
    users_collection.update_one({"_id": current_user["_id"]}, {"$set": current_user})

    # Return the newly-created order
    return new_order_obj

