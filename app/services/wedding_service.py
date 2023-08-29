from sqlalchemy.orm import Session

import app.infrastructure.models.wedding_models as models
from app.entities.wedding.Faq import FaqCreate


def get_faqs(db: Session):
    """Get all FAQs, return a list of FAQs"""
    return db.query(models.FaqModel).all()


def get_faq_by_id(db: Session, faq_id: int):
    """Get an FAQ by it's ID, return the FAQ"""
    return db.query(models.FaqModel).filter(models.FaqModel.id == faq_id).first()


def create_faq(db: Session, faq: FaqCreate):
    """Create an FAQ, return the created FAQ"""
    db_faq = models.FaqModel(question=faq.question, asker_id=faq.asker_id)
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    return db_faq


# def answer_faq(db: Session, faq_id: int, faq: FaqAnswer):
#     """Answer an FAQ by it's ID, return the answered FAQ"""
#     db_faq = db.query(models.Faq).filter(models.Faq.id == faq_id).first()
#     if db_faq is None:
#         raise Exception(f"FAQ with id {faq_id} not found")
#     # if db_faq.answer is not None:
#     #     raise Exception(f"FAQ with id {faq_id} already has an answer")

#     db_faq.answer = faq.answer
#     db_faq.answerer_id = faq.answerer_id
#     db.commit()
#     db.refresh(db_faq)
#     return db_faq


def remove_faq_by_id(db: Session, faq_id: int):
    """Delete an FAQ by it's ID, return the deleted FAQ"""

    db_faq = db.query(models.FaqModel).filter(models.FaqModel.id == faq_id).first()
    db.delete(db_faq)
    db.commit()

    return db_faq
