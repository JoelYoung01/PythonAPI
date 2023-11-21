"""The role models"""
from datetime import datetime
from fastapi_utils.api_model import APIModel


class Role(APIModel):
    """The Role model"""

    role_key: str
    role_name: str

    class Config:
        orm_mode = True


class CreateRole(APIModel):
    """The request for creating a new role"""

    role_key: str
    role_name: str
