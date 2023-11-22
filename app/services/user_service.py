from datetime import datetime, timedelta
import os
import re
from typing import Annotated, List
from dotenv import load_dotenv

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from rsa import verify
from app.entities.role import CreateRole
from app.entities.user import CreateUser, User
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.infrastructure.models.main_models import RoleModel, UserModel
from app.infrastructure.main_database import SessionLocal

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    """The token model"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """The token data model"""

    username: str | None = None


def get_main_db():
    """Get the main database session.

    Yields:
        Any: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: Annotated[str, Depends(oath2_scheme)],
    db: SessionLocal = Depends(get_main_db),
) -> UserModel:
    """Get the current user from the token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password"""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user, returns the user on success and None on fail"""

    user = db.query(UserModel).filter(UserModel.username == username).first()

    if not user:
        return False

    if not verify_password(password, user.password_hash):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)):
    """Create an access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db: Session, username: str) -> UserModel | None:
    """Get a user by their username"""

    return db.query(UserModel).filter(UserModel.username == username).first()


def create_user(db: Session, create_user_request: CreateUser) -> UserModel:
    """Create a user"""

    # If the user already exists, raise an error
    if get_user(db, create_user_request.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(UserModel).filter(UserModel.email == create_user_request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate the user's username
    if not create_user_request.username.isalnum():
        raise HTTPException(
            status_code=400,
            detail="Username must only contain alphanumeric characters",
        )

    # Validate the user's email
    email_re = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_re, create_user_request.email):
        raise HTTPException(
            status_code=400,
            detail="Email must be a valid email address",
        )

    db_user = UserModel(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        preferred_name=create_user_request.preferred_name,
        password_hash=hash_password(create_user_request.password),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_role(db: Session, role_key: str) -> RoleModel | None:
    """Get a role by it's role_key"""

    return db.query(RoleModel).filter(RoleModel.role_key == role_key).first()


def get_roles(db: Session) -> List[RoleModel]:
    """Get all roles"""

    return db.query(RoleModel).all()


def create_role(db: Session, create_role_request: CreateRole) -> RoleModel:
    """Create a role"""

    # If the role already exists, raise an error
    if get_role(db, create_role_request.role_key):
        raise HTTPException(status_code=400, detail="Role already registered")

    # Validate the role's key is alphanumeric, hyphens, or underscores
    if not re.match("^[a-zA-Z0-9_-]*$", create_role_request.role_key):
        raise HTTPException(
            status_code=400,
            detail="Role key must only contain alphanumeric characters, hyphens, or underscores",
        )

    db_role = RoleModel(
        role_key=create_role_request.role_key,
        role_name=create_role_request.role_name,
        created_at=datetime.now(),
    )

    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def add_user_on_role(db: Session, user_id: int, role_key: str) -> None:
    """Add a user to a role"""

    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    db_role = db.query(RoleModel).filter(RoleModel.role_key == role_key).first()
    if not db_role:
        raise HTTPException(status_code=400, detail="Role not found")

    if db_role in db_user.roles:
        raise HTTPException(status_code=400, detail="User already has this role")

    db_user.roles.append(db_role)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user_from_role(db: Session, user_id: int, role_key: str) -> None:
    """Remove a user from a role"""

    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    db_role = db.query(RoleModel).filter(RoleModel.role_key == role_key).first()
    if not db_role:
        raise HTTPException(status_code=400, detail="Role not found")

    if db_role not in db_user.roles:
        raise HTTPException(status_code=400, detail="User does not have this role")

    db_user.roles.remove(db_role)
    db.commit()
    db.refresh(db_user)
    return db_user


def user_has_role(user: UserModel, role_key: str) -> bool:
    """Check if a user has a role"""
    return role_key in [role.role_key for role in user.roles]
