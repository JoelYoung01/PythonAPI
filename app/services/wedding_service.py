from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.infrastructure.models.wedding_models as models
from app.entities.wedding.Faq import FaqAnswer, FaqCreate


def get_faqs(db: Session):
    """Get all FAQs, return a list of FAQs"""

    return db.query(models.FaqModel).all()


def get_faq_by_id(db: Session, faq_id: int):
    """Get an FAQ by it's ID, return the FAQ"""

    return db.query(models.FaqModel).filter(models.FaqModel.id == faq_id).first()


def create_faq(db: Session, faq: FaqCreate):
    """Create an FAQ, return the created FAQ"""

    # Make sure there isn't already a faq with the same question
    duplicates = (
        db.query(models.FaqModel)
        .filter(models.FaqModel.question == faq.question)
        .count()
    )

    if duplicates > 0:
        raise HTTPException(
            status_code=400, detail=f"FAQ with question '{faq.question}' already exists"
        )

    db_faq = models.FaqModel(question=faq.question, asker=faq.asker)
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    return db_faq


def answer_faq(db: Session, faq_id: int, faq: FaqAnswer):
    """Answer an FAQ by it's ID, return the answered FAQ"""

    db_faq = db.query(models.Faq).filter(models.Faq.id == faq_id).first()
    if db_faq is None:
        raise HTTPException(status_code=404, detail=f"FAQ with id {faq_id} not found")
    if db_faq.answer is not None:
        raise HTTPException(
            status_code=400, detail=f"FAQ with id {faq_id} already has an answer"
        )

    db_faq.answer = faq.answer
    db_faq.answerer = faq.answerer
    db.commit()
    db.refresh(db_faq)
    return db_faq


def update_faq(db: Session, faq_id: int, faq: FaqAnswer):
    """Update an FAQ by it's ID, return the updated FAQ"""

    db_faq = db.query(models.FaqModel).filter(models.FaqModel.id == faq_id).first()
    db_faq.question = faq.question or db_faq.question
    db_faq.asker = faq.asker or db_faq.asker
    db_faq.answer = faq.answer or db_faq.answer
    db_faq.answerer = faq.answerer or db_faq.answerer
    db.commit()
    db.refresh(db_faq)
    return db_faq


def remove_faq_by_id(db: Session, faq_id: int):
    """Delete an FAQ by it's ID, return the deleted FAQ"""

    db_faq = db.query(models.FaqModel).filter(models.FaqModel.id == faq_id).first()

    if db_faq is None:
        raise HTTPException(status_code=404, detail=f"FAQ with id {faq_id} not found")

    db.delete(db_faq)
    db.commit()

    return db_faq
