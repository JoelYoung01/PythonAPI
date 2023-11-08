"""Entities related to a Project
"""

from fastapi_utils.api_model import APIModel


class ProjectCreate(APIModel):
    """The payload required to Create a new Project"""

    project_key: str
    title: str
    image_src: str
    source_uri: str
    description: str
    uri: str | None = None


class ProjectUpdate(APIModel):
    """The payload required to Update an existing Project"""

    project_key: str | None = None
    title: str | None = None
    image_src: str | None = None
    source_uri: str | None = None
    description: str | None = None
    uri: str | None = None


class Project(APIModel):
    """The payload returned when a Project is retrieved"""

    project_id: int
    project_key: str
    title: str
    image_src: str
    source_uri: str
    description: str
    uri: str | None = None

    class Config(APIModel.Config):
        """The ProjectConfig is used to configure the Project APIModel."""

        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 24,
                    "projectKey": "project_key",
                    "title": "title",
                    "imageSrc": "image_src",
                    "sourceUri": "source_uri",
                    "description": "description",
                    "uri": "uri",
                },
            ]
        }
