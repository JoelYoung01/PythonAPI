"""Entities related to Albums
"""

from datetime import datetime
from fastapi_utils.api_model import APIModel

from app.entities.photo import Photo


class CreateAlbum(APIModel):
    """The payload used to create an Album"""

    title: str
    description: str | None = None


class UpdateAlbum(APIModel):
    """The payload used to update an Album"""

    title: str | None = None
    description: str | None = None
    cover_photo_id: int | None = None


class Album(APIModel):
    """The payload returned when an Album is retrieved"""

    id: int
    title: str
    description: str | None = None
    cover_photo: Photo | None = None
    photos: list[Photo] = []
    created_at: datetime
    updated_at: datetime

    class Config(APIModel.Config):
        """The AlbumConfig is used to configure the Album APIModel."""

        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "title": "A cool Album of Memes",
                    "description": "This should be a cool album of memes.",
                    "coverPhoto": {
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
                    "photos": [
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
                    ],
                    "createdAt": "2021-01-01T00:00:00.000Z",
                    "updatedAt": "2021-01-01T00:00:00.000Z",
                },
            ]
        }
