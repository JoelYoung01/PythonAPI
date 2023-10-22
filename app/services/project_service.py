from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.infrastructure.models.main_models as models
from app.entities.Project import ProjectCreate, ProjectUpdate


def get_projects(db: Session):
    """Get all Projects, return a list of Projects"""

    return db.query(models.ProjectModel).all()


def get_project_by_id(db: Session, project_id: int):
    """Get a Project by it's ID, return the Project"""

    return (
        db.query(models.ProjectModel)
        .filter(models.ProjectModel.project_id == project_id)
        .first()
    )


def create_project(db: Session, project: ProjectCreate):
    """Create a Project, return the created Project"""

    # Validate the project_key is not empty, and is all lowercase alphanumeric characters or hyphens
    if (
        project.project_key is None
        or not project.project_key.islower()
        or not project.project_key.replace("-", "").isalnum()
    ):
        raise HTTPException(
            status_code=400,
            detail="Project key must be all lowercase alphanumeric characters or hyphens",
        )

    # Validate there isn't already a project with the same key
    duplicates = (
        db.query(models.ProjectModel)
        .filter(models.ProjectModel.project_key == project.project_key)
        .count()
    )

    if duplicates > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Project with key '{project.project_key}' already exists",
        )

    db_project = models.ProjectModel(
        project_key=project.project_key,
        title=project.title,
        image_src=project.image_src,
        source_uri=project.source_uri,
        description=project.description,
        uri=project.uri,
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: ProjectUpdate):
    """Update a Project by it's ID, return the updated Project"""

    # Get the project from the database
    db_project = (
        db.query(models.ProjectModel)
        .filter(models.ProjectModel.project_id == project_id)
        .first()
    )

    # If the project with that key doesn't exist, raise an error
    if db_project is None:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found"
        )

    db_project.project_key = project.project_key or db_project.project_key
    db_project.title = project.title or db_project.title
    db_project.image_src = project.image_src or db_project.image_src
    db_project.source_uri = project.source_uri or db_project.source_uri
    db_project.description = project.description or db_project.description

    # If the project.uri is the empty string, "None" or "null", set it to None
    if project.uri is not None and project.uri.lower() in ["none", "null", ""]:
        db_project.uri = None
    else:
        db_project.uri = project.uri or db_project.uri

    db.commit()
    db.refresh(db_project)
    return db_project


def remove_project_by_id(db: Session, project_id: int):
    """Delete a Project by it's ID, return the deleted Project"""

    db_project = (
        db.query(models.ProjectModel)
        .filter(models.ProjectModel.project_id == project_id)
        .first()
    )

    if db_project is None:
        raise HTTPException(
            status_code=404, detail=f"Project with id {project_id} not found"
        )

    db.delete(db_project)
    db.commit()

    return db_project
