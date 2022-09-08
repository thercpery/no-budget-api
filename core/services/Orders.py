from fastapi.encoders import jsonable_encoder
from typing import List
from ..middlewares import database
from ..models.Order import OrderOneProduct, Order
from ..services import Users, Products, Carts, Email

orders_collection = database.orders_collection
carts_collection = database.carts_collection
users_collection = database.users_collection
products_collection = database.products_collection


def setup_multiple_orders_string(product_data: list):
    products_string = """<ul>"""
    for product in product_data:
        products_string = products_string + f"""<li>{product['name']} - Php. {product['price']}</li>"""

    products_string = products_string + """</ul>"""
    return products_string


async def order_send_email(user_data: dict, order_data: dict):
    if len(order_data["products"]) == 1:
        message_data = {
            "to": [
                {
                    "Email": user_data["email"],
                    "Name": user_data["username"]
                }
            ],
            "subject": "Order confirmation",
            "TextPart": "Greetings! Your order is successful!",
            "HTMLPart": f"""<h3>Hi, {user_data['username']}!</h3>
        <br>
        <p>Thank you for shopping with us!</p>
        <br>
        <p>We confirm that you have ordered the following items with the order number of {order_data["_id"]}:</p>
        <ul>
            <li>{order_data["products"][0]["name"]} - Php. {order_data["products"][0]["price"]}</li>
        </ul>
        <p>Thank you for shopping with us!</p>
                """
        }

    else:
        products_string = setup_multiple_orders_string(product_data=order_data["products"])

        message_data = {
            "to": [
                {
                    "Email": user_data["email"],
                    "Name": user_data["username"]
                }
            ],
            "subject": "Order confirmation",
            "TextPart": "Greetings! Your order is successful!",
            "HTMLPart": f"""<h3>Hi, {user_data['username']}!</h3>
                <br>
                <p>Thank you for shopping with us!</p>
                <br>
                <p>We confirm that you have ordered the following items with the order number of {order_data["_id"]}:</p>
                {products_string}
                <p>Thank you for shopping with us!</p>
                        """
        }

    await Email.send_email(message_data=message_data)


async def get_orders_from_user(user_id: str):
    return list(orders_collection.find({"userId": user_id}))




async def create_order(data: dict, current_user: dict):
    # Store the data variable to an Order model object
    order_obj = Order(
        userId=data["userId"],
        products=data["products"],
        totalPrice=data["totalPrice"]
    )
    # Put the model object to a jsonable_encoder function
    order_data = jsonable_encoder(order_obj)

    # Create new order document
    new_order = orders_collection.insert_one(order_data)

    # Get newly-created order
    new_order_obj = orders_collection.find_one({"_id": new_order.inserted_id})

    # Add new order into the user document
    current_user["orders"].append(new_order_obj)

    # Update user into the database
    current_user["dateUpdated"] = new_order_obj["dateCreated"]
    users_collection.update_one({"_id": current_user["_id"]}, {"$set": current_user})

    # Return newly-created order
    return new_order_obj


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

    new_order_data = await create_order(data=data, current_user=current_user)

    order_created = new_order_data["dateCreated"]

    # Deduct product's quantity by the product_data.quantity
    db_product["quantity"] = db_product["quantity"] - product_data.quantity

    # If db_product's quantity reaches zero, make product["isAvailable"] to false
    if db_product["quantity"] == 0:
        db_product["isAvailable"] = False

    # Update product in the database
    db_product["dateUpdated"] = order_created
    products_collection.update_one({"_id": db_product["_id"]}, {"$set": db_product})

    # Send email confirmation
    await order_send_email(user_data=current_user, order_data=new_order_data)

    # Return the newly-created order
    return new_order_data


async def checkout_from_cart(product_ids: List, username: str):
    # Get user data from db
    current_user = await Users.get_user_by_username(username=username)

    # Create db_products array
    db_matching_products = []

    # Create db_products_from_cart
    db_cart_products = []

    total_price = 0

    # Get cart data that matches current user
    db_cart = await Carts.get_cart_from_user(user_id=current_user["_id"])

    # If cart is empty return false
    if db_cart is None:
        return False

    # Store products from cart into db_product_from_cart that matches the given product ids
    for product_id in product_ids:
        for cart_product in db_cart["products"]:
            if product_id == cart_product["_id"] and cart_product["isAvailable"]:
                db_cart_products.append(cart_product)

                # Compute total price
                total_price += cart_product["price"]

                # Store AVAILABLE matching products from products db to db_matching_products
                db_product = await Products.get_product_by_id(_id=product_id)
                db_matching_products.append(db_product)

    # If cart products is not equal to db_products return false
    if len(product_ids) > len(db_cart_products):
        return False

    # Gather the cart items and current user data and total price into the data variable
    data = {
        "userId": current_user["_id"],
        "products": db_cart_products,
        "totalPrice": total_price
    }

    # Get new order data
    new_order_data = await create_order(data=data, current_user=current_user)

    # Get current time based on the time the order was created
    order_created = new_order_data["dateCreated"]

    deduct_total_price = 0
    for product_id in product_ids:
        for cart_product in db_cart["products"]:
            if product_id == cart_product["_id"]:
                # Put price in a deduct_total_price variable
                deduct_total_price += cart_product["price"]

                # Deduct products quantity
                for db_product in db_matching_products:
                    if db_product["_id"] == cart_product["_id"]:
                        db_product["quantity"] -= cart_product["quantity"]

                        # If db_products quantity reaches zero, make db_products["isAvailable"] false
                        if db_product["quantity"] == 0:
                            db_product["isAvailable"] = False

                        # Update products into the database
                        db_product["dateUpdated"] = order_created
                        products_collection.update_one({"_id": db_product["_id"]}, {"$set": db_product})

                # Remove selected item in the cart
                db_cart["products"].remove(cart_product)

    # If cart products is empty, delete cart
    if len(db_cart["products"]) == 0:
        carts_collection.delete_one({"_id": db_cart["_id"]})

    else:
        # Deduct total price
        db_cart["totalPrice"] -= deduct_total_price

        # Update user's cart
        db_cart["dateUpdated"] = order_created
        carts_collection.update_one({"_id": db_cart["_id"]}, {"$set": db_cart})

    # Send email confirmation
    await order_send_email(user_data=current_user, order_data=new_order_data)

    # Return newly-created order
    return new_order_data


async def checkout_all_items_in_cart(username: str):
    # Get current user data from db
    current_user = await Users.get_user_by_username(username=username)

    # Get cart data from db
    db_cart = await Carts.get_cart_from_user(user_id=current_user["_id"])

    if db_cart is None or db_cart["products"] is None:
        return False

    # Get all products
    db_all_products = list(await Products.get_all_products_available())

    # Gather the cart items and current user data and total price into the data variable
    data = {
        "userId": current_user["_id"],
        "products": db_cart["products"],
        "totalPrice": db_cart["totalPrice"]
    }

    # Get new order data
    new_order_data = await create_order(data=data, current_user=current_user)

    # Get time when the order is created
    order_created = new_order_data["dateCreated"]

    for order_product in new_order_data["products"]:
        for db_product in db_all_products:
            if order_product["_id"] == db_product["_id"]:
                # Deduct product quantity
                db_product["quantity"] -= order_product["quantity"]

                # If db_products quantity reaches zero make db_products["isAvailable"] to zero
                if db_product["quantity"] == 0:
                    db_product["isAvailable"] = False

                # Update products into the database
                db_product["dateUpdated"] = order_created
                products_collection.update_one({"_id": db_product["_id"]}, {"$set": db_product})

    # Delete user cart
    carts_collection.delete_one({"_id": db_cart["_id"]})

    # Send email confirmation
    await order_send_email(user_data=current_user, order_data=new_order_data)

    # Return newly-created order
    return new_order_data
