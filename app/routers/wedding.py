from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.entities.wedding.Faq import Faq, FaqAnswer, FaqCreate, FaqUpdate

load_dotenv()

from app.infrastructure.wedding_database import SessionLocal as wedding_SessionLocal
import app.services.wedding_service as wedding_service


def build_app():
    app = FastAPI()

    # Dependency
    def get_wedding_db():
        db = wedding_SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @app.get("/faq", tags=["wedding"])
    def get_all_faqs(db: Session = Depends(get_wedding_db)) -> List[Faq]:
        return wedding_service.get_faqs(db)

    @app.get("/faq/{faq_id}", tags=["wedding"])
    def get_faq_by_id(faq_id: int, db: Session = Depends(get_wedding_db)) -> Faq:
        faq = wedding_service.get_faq_by_id(db, faq_id)
        if faq is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return faq

    @app.post("/faq", tags=["wedding"])
    def create_faq(faq: FaqCreate, db: Session = Depends(get_wedding_db)) -> Faq:
        return wedding_service.create_faq(db, faq)

    @app.post("/faq/{faq_id}/answer", tags=["wedding"])
    def answer_faq(
        faq_id: int, faq: FaqAnswer, db: Session = Depends(get_wedding_db)
    ) -> Faq:
        return wedding_service.answer_faq(db, faq_id, faq)

    @app.post("/faq/{faq_id}", tags=["wedding"])
    def update_faq(
        faq_id: int, faq: FaqUpdate, db: Session = Depends(get_wedding_db)
    ) -> Faq:
        return wedding_service.update_faq(db, faq_id, faq)

    @app.delete("/faq/{faq_id}", tags=["wedding"])
    def remove_faq_by_id(faq_id: int, db: Session = Depends(get_wedding_db)) -> Faq:
        return wedding_service.remove_faq_by_id(db, faq_id)

    return app
