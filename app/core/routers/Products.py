from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from ..models.Product import ProductBase, ProductUpdate
from ..services import Products

router = APIRouter()


@router.post("/", response_description="Add a new product")
async def add_product(product_data: ProductBase = Body()):
    product = jsonable_encoder(product_data)
    return await Products.add_products(product_data=product)


@router.get("/", response_description="Get all products that are in stock", response_model=List[ProductBase])
async def get_all_products_available():
    return await Products.get_all_products_available()


@router.get("/{_id}", response_description="Get product by ID", response_model=ProductBase)
async def get_product_by_id(_id: str):
    product = await Products.get_available_product_by_id(_id=_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not in our database or not in stock")

    return product


@router.get("/search/{keyword}", response_description="Get products by keyword", response_model=List[ProductBase])
async def get_products_by_keyword(keyword: str):
    products = await Products.get_products_by_keyword(keyword=keyword)
    if products is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not in our database or not in stock")

    return products


@router.patch("/{_id}/shelforresell", response_description="Shelf or resell product")
async def shelf_or_resell_product(_id: str):
    is_product_shelved_or_resold = await Products.shelf_or_resell_product(_id=_id)
    if not is_product_shelved_or_resold:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not in our database or not in stock")

    return is_product_shelved_or_resold


@router.patch("/{_id}", response_description="Update product", response_model=ProductBase)
async def update_product(_id: str, product_data: ProductUpdate = Body()):
    is_item_updated = await Products.update_product(_id=_id, product_data=product_data)
    if not is_item_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not in our database or not in stock")

    return is_item_updated

