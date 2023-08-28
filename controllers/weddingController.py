from fastapi import FastAPI

from models.wedding.faq import Faq


def buildWeddingEndpoints(app: FastAPI):
    @app.get("/wedding/faq", tags=["wedding"])
    def get_all_faqs() -> Faq:
        return []

    @app.get("/wedding/faq/{faq_id}", tags=["wedding"])
    def get_faq_by_id(faq_id: int) -> Faq:
        # raise HTTPException(status_code=404, detail="Item not found")
        return None
