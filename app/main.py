from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.entities.Project import Project, ProjectCreate, ProjectUpdate


load_dotenv()

from app.infrastructure.main_database import SessionLocal
from app.routers.wedding import build_app as build_wedding_app
import app.services.project_service as project_service

# Automatically create a global session to be used by all routes
# Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_main_db():
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
    return RedirectResponse(url="/static/index.html")


# Redirect favicon to static file
@app.get("/favicon.ico", include_in_schema=False)
def read_favicon():
    return RedirectResponse(url="/static/favicon.ico")


# Health Checker Endpoint
@app.get("/health", tags=["health"], include_in_schema=False)
def health():
    return {"status": "ok"}


# Mount any sub-apps
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/wedding", build_wedding_app())

#
# Setup main api routes
#


@app.get("/project", tags=["projects"])
def get_all_projects(db: SessionLocal = Depends(get_main_db)) -> List[Project]:
    return project_service.get_projects(db)


@app.get("/project/{project_id}", tags=["projects"])
def get_project_by_id(
    project_id: int, db: SessionLocal = Depends(get_main_db)
) -> Project:
    project = project_service.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=404, detail=f"Project not found with an ID of {project_id}"
        )
    return project


@app.put("/project/{project_id}", tags=["projects"])
def update_project(
    project_id: int,
    updated_project: ProjectUpdate,
    db: SessionLocal = Depends(get_main_db),
) -> Project:
    """
    Update a Project by it's ID, returns the updated Project.
    To update a nullable value to be empty, use an empty string, "null", or "none".
    """
    return project_service.update_project(db, project_id, updated_project)


@app.delete("/project/{project_id}", tags=["projects"])
def remove_project_by_id(
    project_id: int, db: SessionLocal = Depends(get_main_db)
) -> Project:
    return project_service.remove_project_by_id(db, project_id)


@app.post("/project", tags=["projects"])
def create_project(
    project: ProjectCreate, db: SessionLocal = Depends(get_main_db)
) -> Project:
    return project_service.create_project(db, project)
