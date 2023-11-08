"""Entities related to Photos
"""

from datetime import datetime
from fastapi_utils.api_model import APIModel


class CreatePhoto(APIModel):
    """The payload used to create a Photo"""

    filename: str
    title: str | None = None
    description: str | None = None
    url: str | None = None
    width: int | None = None
    height: int | None = None
    format: str | None = None
    upload_date: datetime = datetime.now()


class Photo(APIModel):
    """The payload returned when a Photo is retrieved"""

    id: int
    filename: str
    title: str | None = None
    description: str | None = None
    url: str | None = None
    width: int | None = None
    height: int | None = None
    format: str | None = None
    upload_date: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config(APIModel.Config):
        """The PhotoConfig is used to configure the Photo APIModel."""

        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "filename": "img-ljkwenasdoiiaoc89923n.wepb",
                    "title": "A Good Meme",
                    "description": "This is a good meme.",
                    "url": "example.com/images/img-ljkwenasdoiiaoc89923n.wepb",
                    "width": 64,
                    "height": 64,
                    "uploadDate": "2021-01-01T00:00:00.000Z",
                    "format": "format",
                    "createdAt": "2021-01-01T00:00:00.000Z",
                    "updatedAt": "2021-01-01T00:00:00.000Z",
                },
            ]
        }
