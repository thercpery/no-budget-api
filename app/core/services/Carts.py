from fastapi.encoders import jsonable_encoder
from datetime import datetime
from ..middlewares import database
from ..models.Cart import CartItems
from ..services import Products

carts_collection = database.carts_collection
products_collection = database.products_collection


async def search_from_cart_products_list(
        cart_products: list,
        product_id: str,
        product_quantity: int,
        product_price: float):
    for cart_product in cart_products:
        if cart_product["_id"] == product_id:
            cart_product["quantity"] += product_quantity
            cart_product["price"] += product_price
            return cart_products

    return False


async def get_cart_from_user(user_id: str):
    return carts_collection.find_one({"userId": user_id})


async def add_product_to_cart(product_id: str, quantity: int, user_id: str):
    db_product = await Products.get_product_by_id(_id=product_id)
    if db_product is None or not db_product["isAvailable"]:
        return False

    del db_product["description"]
    del db_product["categories"]
    del db_product["isAvailable"]
    del db_product["dateCreated"]
    del db_product["dateUpdated"]
    db_product["quantity"] = quantity
    db_product["price"] = db_product["price"] * quantity

    db_cart = await get_cart_from_user(user_id=user_id)

    if db_cart is None:
        product_arr = [db_product]
        cart_item_obj = CartItems(
            userId=user_id,
            products=product_arr,
            totalPrice=db_product["price"]
        )
        cart_data = jsonable_encoder(cart_item_obj)

        carts_collection.insert_one(cart_data)

    else:
        updated_products_data = await search_from_cart_products_list(
            cart_products=db_cart["products"],
            product_id=db_product["_id"],
            product_quantity=quantity,
            product_price=db_product["price"]
        )

        if not updated_products_data:
            db_cart["products"].append(db_product)
        else:
            db_cart["products"] = updated_products_data

        db_cart["totalPrice"] += db_product["price"]
        db_cart["dateUpdated"] = datetime.now()

        carts_collection.update_one({"_id": db_cart["_id"]}, {"$set": db_cart})

    display_cart = await get_cart_from_user(user_id=user_id)
    return display_cart

