from sqlalchemy import Column, Integer, String

from app.infrastructure.main_database import Base


class FaqModel(Base):
    __tablename__ = "faq"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255))
    answer = Column(String(255), nullable=True)
    asker_id = Column(Integer, nullable=True)
    answerer_id = Column(Integer, nullable=True)
