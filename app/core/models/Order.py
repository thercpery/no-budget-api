from mongoengine import *
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from typing import List


class Order(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    userId: str = StringField()
    products: List[dict] = Field(default=[])
    totalPrice: float = FloatField()
    dateCreated: datetime = Field(default=datetime.utcnow())
    dateUpdated: datetime = Field(default=datetime.utcnow())

    class Config:
        allow_population_by_field_name = True


class OrderOneProduct(BaseModel):
    product_id: str = Field()
    quantity: int = Field()


class CheckoutFromCart(BaseModel):
    product_ids: List[str] = Field()
