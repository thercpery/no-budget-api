from mongoengine import *
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List
from datetime import datetime


class Cart(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    userId: str = StringField()
    products: List[dict] = Field(default=[])
    totalPrice: float = FloatField()
    date

