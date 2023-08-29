from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.main_database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    key = Column(String)
    imageSrc = Column(String)
    gitUri = Column(String)
    projectUri = Column(String)


class PersonalContactModel(Base):
    __tablename__ = "personalContacts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    icon = Column(String)


class SkillModel(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    type = Column(String)
    mdiIcon = Column(String)


class SocialMediaModel(Base):
    __tablename__ = "socials"

    id = Column(Integer, primary_key=True, index=True)
    profileUri = Column(String)
    profileImageUri = Column(String)
    mdiIcon = Column(String)
    handle = Column(String)


class HobbyModel(Base):
    __tablename__ = "hobbies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    imageSrc = Column(String)
