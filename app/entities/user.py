"""The user models"""
from fastapi_utils.api_model import APIModel


class User(APIModel):
    username: str
    email: str
    first_name: str
    last_name: str
    preferred_name: str | None = None


class CreateUser(APIModel):
    username: str
    email: str
    first_name: str
    last_name: str
    preferred_name: str | None = None
    password: str
