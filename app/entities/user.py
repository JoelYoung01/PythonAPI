"""The user models"""
from typing import List
from fastapi_utils.api_model import APIModel

from app.entities.role import Role


class User(APIModel):
    username: str
    email: str
    first_name: str
    last_name: str
    preferred_name: str | None = None
    roles: List[Role]

    class Config:
        orm_mode = True


class CreateUser(APIModel):
    username: str
    email: str
    first_name: str
    last_name: str
    preferred_name: str | None = None
    password: str
