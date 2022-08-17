from mongoengine import *
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List, Optional


class UserBase(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    username: str = StringField(required=True)
    email: str = StringField(required=True)
    password: str = StringField(required=True)
    mobileNo: str = StringField(required=True)
    address: str = StringField(required=True)
    isAdmin: bool = Field(default=False)
    orders: List[dict] = Field(default=[])
    dateCreated: datetime = Field(default=datetime.utcnow())
    dateUpdated: datetime = Field(default=datetime.utcnow())

    class Config:
        allow_population_by_field_name = True


class UserDisplay(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    username: str = StringField(required=True)
    email: str = StringField(required=True)
    mobileNo: str = StringField(required=True)
    address: str = StringField(required=True)
    isAdmin: bool = Field(default=False)
    orders: List[dict] = Field(default=[])
    dateCreated: datetime = Field(default=datetime.utcnow())
    dateUpdated: datetime = Field(default=datetime.utcnow())


class LoginUser(BaseModel):
    username: str = Field()
    password: str = Field()


class UserChangePassword(BaseModel):
    current_password: str = Field()
    new_password: str = Field()


class UserChangeUsername(BaseModel):
    username: str = Field()


class UserGrantOrRevokeAdminAccess(BaseModel):
    username: str = Field()
