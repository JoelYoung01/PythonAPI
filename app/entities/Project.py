from pydantic import BaseModel


class ProjectCreate(BaseModel):
    """The payload required to Create a new Project"""

    project_key: str
    title: str
    image_src: str
    source_uri: str
    description: str
    uri: str | None = None


class ProjectUpdate(BaseModel):
    """The payload required to Update an existing Project"""

    project_key: str | None = None
    title: str | None = None
    image_src: str | None = None
    source_uri: str | None = None
    description: str | None = None
    uri: str | None = None


class Project(BaseModel):
    """The payload returned when a Project is retrieved"""

    project_id: int
    project_key: str
    title: str
    image_src: str
    source_uri: str
    description: str
    uri: str | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 24,
                    "project_key": "project_key",
                    "title": "title",
                    "image_src": "image_src",
                    "source_uri": "source_uri",
                    "description": "description",
                    "uri": "uri",
                },
            ]
        }
