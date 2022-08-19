from mongoengine import *
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List, Optional


class ProductBase(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    name: str = StringField(required=True)
    description: str = StringField(required=True)
    categories: List[str] = ListField(StringField(required=True))
    sku: str = StringField(required=True)
    quantity: int = IntField(required=True)
    price: float = FloatField(required=True)
    isAvailable: bool = Field(default=True)
    dateCreated: datetime = Field(default=datetime.utcnow())
    dateUpdated: datetime = Field(default=datetime.utcnow())

    class Config:
        allow_population_by_field_name = True
        schema_example = {
            "example": {
                "id": "c02796fb-26b3-47dd-a0ee-75a56e54ca51",
                "name": "Samsung Galaxy S5",
                "description": "Old, but reliable",
                "categories": ["Smartphones"],
                "sku": "123456",
                "quantity": 100,
                "price": 1000.00,
                "isAvailable": True,
                "dateCreated": datetime.utcnow(),
                "dateUpdated": datetime.utcnow()
            }
        }


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    categories: Optional[List[str]]
    sku: Optional[str]
    quantity: Optional[int]
    price: Optional[float]

    class Config:
        schema_example = {
            "example": {
                "name": "Samsung Galaxy S5",
                "description": "Old, but reliable",
                "category": "",
                "sku": "123456",
                "quantity": 100,
                "price": 1000.00
            }
        }
