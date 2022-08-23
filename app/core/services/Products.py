from typing import List
from ..middlewares import database
from ..models.Product import ProductBase

products_collection = database.products_collection


async def get_all_products_available() -> List[ProductBase]:
    return list(products_collection.find({"isAvailable": True}))


async def get_product_by_id(_id: str) -> ProductBase:
    return products_collection.find_one({"_id": _id})


async def get_available_product_by_id(_id: str) -> ProductBase:
    return products_collection.find_one({"_id": _id, "isAvailable": True})


async def get_products_by_keyword(keyword: str) -> List[ProductBase]:
    return list(products_collection.find({"$text": {"$search": keyword}, "isAvailable": True}))


