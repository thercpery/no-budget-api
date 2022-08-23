from fastapi import APIRouter, Body, HTTPException, status, Depends
from typing import List

from ..models.Product import ProductBase, ProductUpdate
from ..services import Products
from ..services import Users

router = APIRouter()


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



