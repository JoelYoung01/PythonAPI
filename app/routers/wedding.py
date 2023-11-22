from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.entities.wedding.Faq import Faq, FaqCreate, FaqUpdate
from app.infrastructure.models.main_models import UserModel

load_dotenv()

from app.infrastructure.wedding_database import SessionLocal as wedding_SessionLocal
from app.services import wedding_service, user_service

modify_role = "GENERAL_MODIFY"


def build_app(oath2_scheme):
    app = FastAPI()

    # Dependency
    def get_wedding_db():
        db = wedding_SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @app.get("/faq", tags=["Wedding"])
    def get_all_faqs(db: Session = Depends(get_wedding_db)) -> List[Faq]:
        """Get all FAQs"""
        return wedding_service.get_faqs(db)

    @app.get("/faq/{faq_id}", tags=["Wedding"])
    def get_faq_by_id(faq_id: int, db: Session = Depends(get_wedding_db)) -> Faq:
        """Get a single FAQ by it's ID"""
        faq = wedding_service.get_faq_by_id(db, faq_id)
        if faq is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return faq

    @app.post("/faq", tags=["Wedding"])
    def create_faq(
        faq: FaqCreate,
        current_user: Annotated[UserModel, Depends(user_service.get_current_user)],
        db: Session = Depends(get_wedding_db),
    ) -> Faq:
        """Create a new FAQ"""

        if not user_service.user_has_role(current_user, modify_role):
            raise HTTPException(
                status_code=403,
                detail="User does not have permission to create FAQs",
            )

        return wedding_service.create_faq(db, faq)

    @app.put("/faq/{faq_id}", tags=["Wedding"])
    def update_faq(
        faq_id: int,
        faq: FaqUpdate,
        current_user: Annotated[UserModel, Depends(user_service.get_current_user)],
        db: Session = Depends(get_wedding_db),
    ) -> Faq:
        """
        Update an existing FAQ by it's ID, returns the updated Faq.
        To update a nullable value to be empty, use an empty string, "null", or "none".
        """

        if not user_service.user_has_role(current_user, modify_role):
            raise HTTPException(
                status_code=403,
                detail="User does not have permission to update FAQs",
            )

        return wedding_service.update_faq(db, faq_id, faq)

    @app.delete("/faq/{faq_id}", tags=["Wedding"])
    def remove_faq_by_id(
        faq_id: int,
        current_user: Annotated[UserModel, Depends(user_service.get_current_user)],
        db: Session = Depends(get_wedding_db),
    ) -> Faq:
        """Remove an existing FAQ by it's ID"""

        if not user_service.user_has_role(current_user, modify_role):
            raise HTTPException(
                status_code=403,
                detail="User does not have permission to remove FAQs",
            )

        return wedding_service.remove_faq_by_id(db, faq_id)

    return app
