from mongoengine import *
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, timedelta


class Confirmation(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    userId: str = Field()
    isConfirmed: str = Field(default=False)
    expireAt: datetime = Field(default=datetime.now() + timedelta(minutes=30))
    dateCreated: datetime = Field(default=datetime.now())
    dateUpdated: datetime = Field(default=datetime.now())

    class Config:
        allow_population_by_field_name = True
