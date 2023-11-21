"""_summary_: The ProjectModel is used to represent a Project in the database.
"""
from venv import create
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.infrastructure.main_database import Base


class UserModel(Base):
    """User Model"""

    __tablename__ = "Users"

    user_id = Column("id", Integer, primary_key=True, index=True)
    username = Column("username", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    first_name = Column("firstname", String(255), nullable=False)
    last_name = Column("lastname", String(255), nullable=False)
    preferred_name = Column("preferredname", String(255), nullable=True)
    password_hash = Column("passwordhash", String(255), nullable=False)
    created_at = Column("created_at", Date, nullable=True)
    updated_at = Column("updated_at", Date, nullable=True)


class ProjectModel(Base):
    """Project Model"""

    __tablename__ = "Projects"

    project_id = Column("ProjectID", Integer, primary_key=True, index=True)
    project_key = Column("ProjectKey", String(255), nullable=False)
    title = Column("Title", String(255), nullable=False)
    image_src = Column("ImageSrc", String(1023), nullable=False)
    source_uri = Column("SourceUri", String(1023), nullable=False)
    description = Column("Description", String, nullable=False)
    uri = Column("Uri", String(1023), nullable=True)


# Many to Many relationship between Album and Photo
album_photo = Table(
    "AlbumPhoto",
    Base.metadata,
    Column("photo_id", Integer, ForeignKey("Photo.id")),
    Column("album_id", Integer, ForeignKey("Album.id")),
)


class PhotoModel(Base):
    """Photo Model"""

    __tablename__ = "Photo"

    id = Column("id", Integer, primary_key=True, index=True)
    filename = Column("filename", String(255), nullable=False)
    title = Column("title", String(255), nullable=True)
    description = Column("description", String, nullable=True)
    url = Column("url", String(255), nullable=True)
    width = Column("width", Integer, nullable=True)
    height = Column("height", Integer, nullable=True)
    upload_date = Column("upload_date", Date, nullable=True)
    format = Column("format", String(10), nullable=True)
    created_at = Column("created_at", Date, nullable=True)
    updated_at = Column("updated_at", Date, nullable=True)


class AlbumModel(Base):
    """Album Model"""

    __tablename__ = "Album"

    id = Column("id", Integer, primary_key=True, index=True)
    title = Column("title", String(255), nullable=False)
    description = Column("description", String, nullable=True)
    cover_photo_id = Column(Integer, ForeignKey("Photo.id"), nullable=True)
    created_at = Column("created_at", Date, nullable=True)
    updated_at = Column("updated_at", Date, nullable=True)

    cover_photo = relationship("PhotoModel")
    photos = relationship("PhotoModel", secondary=album_photo)


# class PersonalContactModel(Base):
#     __tablename__ = "personalContacts"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     icon = Column(String)


# class SkillModel(Base):
#     __tablename__ = "skills"

#     id = Column(Integer, primary_key=True, index=True)
#     description = Column(String)
#     type = Column(String)
#     mdiIcon = Column(String)


# class SocialMediaModel(Base):
#     __tablename__ = "socials"

#     id = Column(Integer, primary_key=True, index=True)
#     profileUri = Column(String)
#     profileImageUri = Column(String)
#     mdiIcon = Column(String)
#     handle = Column(String)


# class HobbyModel(Base):
#     __tablename__ = "hobbies"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     description = Column(String)
#     imageSrc = Column(String)
