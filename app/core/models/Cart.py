from mongoengine import *
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List
from datetime import datetime


class CartItems(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    userId: str = StringField()
    products: List[dict] = Field(default=[])
    totalPrice: float = FloatField()
    dateCreated: datetime = Field(default=datetime.now())
    dateUpdated: datetime = Field(default=datetime.now())


class AddToCart(BaseModel):
    product_id: str = Field()
    quantity: int = Field()
