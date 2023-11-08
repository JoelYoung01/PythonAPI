"""Photo Service, contains logic for interacting with Photos in the database.
"""

from datetime import datetime
from pathlib import Path
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.entities.album import CreateAlbum, UpdateAlbum
from app.entities.photo import CreatePhoto, UpdatePhoto
import app.infrastructure.models.main_models as models
from app.services.utils import get_updated_value


def get_photos(db: Session) -> list[models.PhotoModel]:
    """Get all Photos, return a list of Photos

    Args:
        db (Session): Database

    Returns:
        List[PhotoModel]: List of all Photos in Database
    """

    return db.query(models.PhotoModel).all()


def get_photo_by_id(db: Session, photo_id: int) -> models.PhotoModel:
    """Get a Photo by it's ID, return the Photo

    Args:
        db (Session): Database
        photo_id (int): ID of the Photo to retrieve

    Returns:
        PhotoModel: The Photo retrieved from the database
    """

    photo = db.query(models.PhotoModel).filter(models.PhotoModel.id == photo_id).first()

    if not photo:
        raise HTTPException(
            status_code=404, detail=f"Photo with ID {photo_id} does not exist"
        )

    return photo


def get_photo_by_filename(db: Session, photo_filename: str) -> models.PhotoModel:
    """Get a Photo by it's filename, return the Photo

    Args:
        db (Session): Database
        photo_filename (str): Filename of the Photo to retrieve

    Returns:
        PhotoModel: The Photo retrieved from the database
    """

    photo = (
        db.query(models.PhotoModel)
        .filter(models.PhotoModel.filename == photo_filename)
        .first()
    )

    if not photo:
        raise HTTPException(
            status_code=404,
            detail=f"Photo with filename {photo_filename} does not exist",
        )

    return photo


def create_photo(db: Session, photo: CreatePhoto) -> models.PhotoModel:
    """Create a new Photo, return the Photo

    Args:
        db (Session): Database
        photo (CreatePhoto): Photo to create

    Returns:
        PhotoModel: The Photo created in the database
    """

    same_filename = (
        db.query(models.PhotoModel)
        .filter(models.PhotoModel.filename == photo.filename)
        .first()
    )

    if same_filename:
        raise HTTPException(
            status_code=409,
            detail=f"Photo with filename {photo.filename} already exists",
        )

    if not verify_photo_file_exists(photo.filename):
        raise HTTPException(
            status_code=409,
            detail=f"Photo with filename {photo.filename} doesn't exist on disk",
        )

    new_photo = models.PhotoModel(
        filename=photo.filename,
        title=photo.title,
        description=photo.description,
        url=photo.url,
        width=photo.width,
        height=photo.height,
        upload_date=photo.upload_date,
        format=photo.format,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )

    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return new_photo


def update_photo(db: Session, photo_id: int, photo: UpdatePhoto) -> models.PhotoModel:
    """Update a Photo by it's ID, return the updated Photo

    Args:
        db (Session): Database
        photo_id (int): ID of the Photo to update
        photo (UpdatePhoto): Photo to update

    Returns:
        PhotoModel: The Photo updated in the database
    """

    db_photo = (
        db.query(models.PhotoModel).filter(models.PhotoModel.id == photo_id).first()
    )

    if not db_photo:
        raise HTTPException(
            status_code=404, detail=f"Photo with ID {photo_id} does not exist"
        )

    if photo.filename:
        if not verify_photo_file_exists(photo.filename):
            raise HTTPException(
                status_code=409,
                detail=f"Photo with filename {photo.filename} doesn't exist on disk",
            )

        if (
            db.query(models.PhotoModel)
            .filter(models.PhotoModel.filename == photo.filename)
            .first()
        ):
            raise HTTPException(
                status_code=409,
                detail=f"Photo with filename {photo.filename} already exists in the database",
            )

    db_photo.filename = photo.filename or db_photo.filename

    db_photo.title = get_updated_value(db_photo.title, photo.title)
    db_photo.description = get_updated_value(db_photo.description, photo.description)
    db_photo.url = get_updated_value(db_photo.url, photo.url)
    db_photo.width = get_updated_value(db_photo.width, photo.width)
    db_photo.height = get_updated_value(db_photo.height, photo.height)
    db_photo.format = get_updated_value(db_photo.format, photo.format)
    db_photo.upload_date = get_updated_value(db_photo.upload_date, photo.upload_date)

    db_photo.updated_at = datetime.now()

    db.commit()
    db.refresh(db_photo)

    return db_photo


def get_albums(db: Session) -> list[models.AlbumModel]:
    """Get all Albums, return a list of Albums

    Args:
        db (Session): Database

    Returns:
        List[AlbumModel]: List of all Albums in Database
    """

    return db.query(models.AlbumModel).all()


def get_album_by_id(db: Session, album_id: int) -> models.AlbumModel:
    """Get an Album by it's ID, return the Album

    Args:
        db (Session): Database
        album_id (int): ID of the Album to retrieve

    Returns:
        AlbumModel: The Album retrieved from the database
    """

    album = db.query(models.AlbumModel).filter(models.AlbumModel.id == album_id).first()

    if not album:
        raise HTTPException(
            status_code=404, detail=f"Album with ID {album_id} does not exist"
        )

    return album


def get_album_by_title(db: Session, album_title: str) -> models.AlbumModel:
    """Get an Album by it's title, return the Album

    Args:
        db (Session): Database
        album_title (str): Title of the Album to retrieve

    Returns:
        AlbumModel: The Album retrieved from the database
    """

    album = (
        db.query(models.AlbumModel)
        .filter(models.AlbumModel.title == album_title)
        .first()
    )

    if not album:
        raise HTTPException(
            status_code=404, detail=f"Album with title {album_title} does not exist"
        )

    return album


def create_album(db: Session, album: CreateAlbum) -> models.AlbumModel:
    """Create a new Album, return the Album

    Args:
        db (Session): Database
        album (CreateAlbum): Album to create

    Returns:
        AlbumModel: The Album created in the database
    """

    # If an album exists with the same title, throw a 409 Conflict
    same_title = (
        db.query(models.AlbumModel)
        .filter(models.AlbumModel.title == album.title)
        .first()
    )

    if same_title:
        raise HTTPException(
            status_code=409, detail=f"Album with title {album.title} already exists"
        )

    new_album = models.AlbumModel(
        title=album.title,
        description=album.description,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )

    db.add(new_album)
    db.commit()
    db.refresh(new_album)

    return new_album


def update_album(db: Session, album_id: int, album: UpdateAlbum) -> models.AlbumModel:
    """Update an Album by it's ID, return the updated Album

    Args:
        db (Session): Database
        album_id (int): ID of the Album to update
        album (UpdateAlbum): Album to update

    Returns:
        AlbumModel: The Album updated in the database
    """

    db_album = (
        db.query(models.AlbumModel).filter(models.AlbumModel.id == album_id).first()
    )

    if not db_album:
        raise HTTPException(
            status_code=404, detail=f"Album with ID {album_id} does not exist"
        )

    db_album.title = get_updated_value(db_album.title, album.title)
    db_album.description = get_updated_value(db_album.description, album.description)

    if album.cover_photo_id:
        cover_photo = (
            db.query(models.PhotoModel)
            .filter(models.PhotoModel.id == album.cover_photo_id)
            .first()
        )

        if not cover_photo:
            raise HTTPException(
                status_code=404,
                detail=f"Photo with ID {album.cover_photo_id} does not exist",
            )

        db_album.cover_photo = cover_photo

    db_album.updated_at = datetime.now()

    db.commit()
    db.refresh(db_album)

    return db_album


def add_photos_to_album(
    db: Session, album_id: int, photo_ids: [int]
) -> models.AlbumModel:
    """Add a list of Photos to an Album, return the Album

    Args:
        db (Session): Database
        album_id (int): ID of the Album to add Photos to
        photo_ids ([int]): List of Photo IDs to add to the Album

    Returns:
        AlbumModel: The Album with the Photos added
    """

    if not photo_ids:
        raise HTTPException(status_code=400, detail="Photo IDs must be provided")

    album = db.query(models.AlbumModel).filter(models.AlbumModel.id == album_id).first()

    if not album:
        raise HTTPException(
            status_code=404, detail=f"Album with ID {album_id} does not exist"
        )

    for photo_id in photo_ids:
        photo = (
            db.query(models.PhotoModel).filter(models.PhotoModel.id == photo_id).first()
        )

        if not photo:
            raise HTTPException(
                status_code=404, detail=f"Photo with ID {photo_id} does not exist"
            )

        if photo.id in [photo.id for photo in album.photos]:
            raise HTTPException(
                status_code=409,
                detail=f"Photo with ID {photo_id} is already in Album with ID {album_id}",
            )

        album.photos.append(photo)

    db.commit()
    db.refresh(album)

    return album


def verify_photo_file_exists(filename: str) -> bool:
    """Verify that a Photo file exists

    Args:
        filename (str): Filename of the Photo to verify

    Returns:
        bool: True if the Photo file exists, False if it does not
    """

    photo_path = f"app/static/images/{filename}"
    return Path(photo_path).is_file()
