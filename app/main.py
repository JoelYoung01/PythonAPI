"""Main FastAPI application module.
"""

from datetime import timedelta
from typing import Annotated, Dict, List
from fastapi import FastAPI, HTTPException
from fastapi import Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.entities.photo import CreatePhoto, Photo, UpdatePhoto
from app.entities.album import Album, CreateAlbum
from app.entities.project import Project, ProjectCreate, ProjectUpdate
from app.entities.role import CreateRole, Role
from app.entities.user import CreateUser, User

from app.infrastructure.main_database import SessionLocal
from app.routers.wedding import build_app as build_wedding_app
from app.services import project_service, photo_service, user_service
from app.services.user_service import oath2_scheme, get_current_user

# Automatically create a global session to be used by all routes
# Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
# Routes
#


# Redirect root to index.html
@app.get("/", include_in_schema=False)
def read_root():
    """Redirect root to index.html"""
    return RedirectResponse(url="/static/index.html")


# Redirect favicon to static file
@app.get("/favicon.ico", include_in_schema=False)
def read_favicon():
    """Redirect favicon to static file"""
    return RedirectResponse(url="/static/favicon.ico")


# Health Checker Endpoint
@app.get("/health", tags=["health"], include_in_schema=False)
def health():
    """Health Checker Endpoint"""
    return {"status": "ok"}


# Mount any sub-apps
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/wedding", build_wedding_app(oath2_scheme=oath2_scheme))

#
# User Routes
#


@app.post("/token", tags=["Users"])
async def login(
    db: Annotated[SessionLocal, Depends(get_main_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Dict[str, str]:
    """Login and get a token"""
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = user_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", tags=["Users"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Read the current user"""
    return current_user


@app.post("/users", tags=["Users"])
def create_user(user: CreateUser, db: SessionLocal = Depends(get_main_db)) -> User:
    """Create a new User"""
    return user_service.create_user(db, user)


@app.get("/roles", tags=["Users"])
def get_all_roles(db: SessionLocal = Depends(get_main_db)) -> List[Role]:
    """Get all Roles"""
    return user_service.get_roles(db)


@app.post("/roles", tags=["Users"])
def create_role(
    role: CreateRole,
    current_user: Annotated[User, Depends(get_current_user)],
    db: SessionLocal = Depends(get_main_db),
) -> Role:
    """Create a new Role"""
    return user_service.create_role(db, role)


@app.post("/users/addRole/{user_id}", tags=["Users"])
def add_role_to_user(
    user_id: int,
    role_key: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: SessionLocal = Depends(get_main_db),
) -> User:
    """Add a Role to a User"""
    return user_service.add_user_on_role(db, user_id, role_key)


#
# Project Routes
#


@app.get("/project", tags=["Projects"])
def get_all_projects(db: SessionLocal = Depends(get_main_db)) -> List[Project]:
    """Get all Projects"""
    return project_service.get_projects(db)


@app.get("/project/{project_id}", tags=["Projects"])
def get_project_by_id(
    project_id: int, db: SessionLocal = Depends(get_main_db)
) -> Project:
    """Get a Project by it's ID"""
    project = project_service.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=404, detail=f"Project not found with an ID of {project_id}"
        )
    return project


@app.put("/project/{project_id}", tags=["Projects"])
def update_project(
    project_id: int,
    updated_project: ProjectUpdate,
    db: SessionLocal = Depends(get_main_db),
) -> Project:
    """Update a Project by it's ID.
    To set an optional value to null/None, pass "null" or "None" as the value."""
    return project_service.update_project(db, project_id, updated_project)


@app.delete("/project/{project_id}", tags=["Projects"])
def remove_project_by_id(
    project_id: int, db: SessionLocal = Depends(get_main_db)
) -> Project:
    """Delete a Project by it's ID"""
    return project_service.remove_project_by_id(db, project_id)


@app.post("/project", tags=["Projects"])
def create_project(
    project: ProjectCreate, db: SessionLocal = Depends(get_main_db)
) -> Project:
    """Create a new Project"""
    return project_service.create_project(db, project)


#
# Photo Routes
#


@app.get("/photo", tags=["Photos"])
def get_all_photos(db: SessionLocal = Depends(get_main_db)) -> List[Photo]:
    """Get all Photos"""

    return photo_service.get_photos(db)


@app.get("/album", tags=["Photos"])
def get_all_albums(db: SessionLocal = Depends(get_main_db)) -> List[Album]:
    """Get all Photos"""

    return photo_service.get_albums(db)


@app.get("/photo/{photo_id}", tags=["Photos"])
def get_photo_by_id(photo_id: int, db: SessionLocal = Depends(get_main_db)) -> Photo:
    """Get a Photo by it's ID"""
    return photo_service.get_photo_by_id(db, photo_id)


@app.get("/photo/filename/{photo_filename}", tags=["Photos"])
def get_photo_by_filename(
    photo_filename: str, db: SessionLocal = Depends(get_main_db)
) -> Photo:
    """Get a Photo by it's filename"""
    return photo_service.get_photo_by_filename(db, photo_filename)


@app.get("/album/title/{album_title}", tags=["Photos"])
def get_album_by_title(
    album_title: str, db: SessionLocal = Depends(get_main_db)
) -> Album:
    """Get an Album by it's title"""
    return photo_service.get_album_by_title(db, album_title)


@app.get("/album/{album_id}/photos", tags=["Photos"])
def get_photos_by_album_id(
    album_id: int, db: SessionLocal = Depends(get_main_db)
) -> List[Photo]:
    """Get all Photos in an Album"""
    album = photo_service.get_album_by_id(db, album_id)
    return album.photos


@app.get("/album/{album_id}", tags=["Photos"])
def get_album_by_id(album_id: int, db: SessionLocal = Depends(get_main_db)) -> Album:
    """Get an Album by it's ID"""
    return photo_service.get_album_by_id(db, album_id)


@app.post("/photo", tags=["Photos"])
def create_photo(photo: CreatePhoto, db: SessionLocal = Depends(get_main_db)) -> Photo:
    """Create a new Photo"""
    return photo_service.create_photo(db, photo)


@app.post("/album", tags=["Photos"])
def create_album(album: CreateAlbum, db: SessionLocal = Depends(get_main_db)) -> Album:
    """Create a new Album"""
    return photo_service.create_album(db, album)


@app.post("/album/addphotos/{album_id}", tags=["Photos"])
def add_photo_to_album(
    album_id: int, photo_ids: List[int], db: SessionLocal = Depends(get_main_db)
) -> Album:
    """Add a Photo to an Album"""
    return photo_service.add_photos_to_album(db, album_id, photo_ids)


@app.put("/photo/{photo_id}", tags=["Photos"])
def update_photo(
    photo_id: int, updated_photo: UpdatePhoto, db: SessionLocal = Depends(get_main_db)
) -> Photo:
    """Update a Photo by it's ID.
    To set an optional value to null/None, pass "null" or "None" as the value."""
    return photo_service.update_photo(db, photo_id, updated_photo)


@app.put("/album/{album_id}", tags=["Photos"])
def update_album(
    album_id: int, updated_album: CreateAlbum, db: SessionLocal = Depends(get_main_db)
) -> Album:
    """Update a Album by it's ID.
    To set an optional value to null/None, pass "null" or "None" as the value."""
    return photo_service.update_album(db, album_id, updated_album)
