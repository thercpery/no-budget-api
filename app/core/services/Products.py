from typing import List
from datetime import datetime
from ..middlewares import database
from ..models.Product import ProductBase

products_collection = database.products_collection


async def add_products(product_data: dict):
    new_product = products_collection.insert_one(product_data)
    created_product = products_collection.find_one({"_id": new_product.inserted_id})

    return created_product


async def get_all_products_available() -> List[ProductBase]:
    return list(products_collection.find({"isAvailable": True}))


async def get_product_by_id(_id: str) -> ProductBase:
    return products_collection.find_one({"_id": _id})


async def get_available_product_by_id(_id: str) -> ProductBase:
    return products_collection.find_one({"_id": _id, "isAvailable": True})


async def get_products_by_keyword(keyword: str) -> List[ProductBase]:
    return list(products_collection.find({"$text": {"$search": keyword}, "isAvailable": True}))


async def update_product():
    pass


async def shelf_or_resell_product(_id: str):
    product = await get_product_by_id(_id=_id)
    if product is None:
        return False

    product["isAvailable"] = not product["isAvailable"]
    product["dateUpdated"] = datetime.now()
    products_collection.update_one({"_id": _id}, {"$set": product})
    return await get_product_by_id(_id=_id)


