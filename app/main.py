from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.entities.wedding.Faq import Faq

load_dotenv()

from app.infrastructure.main_database import engine, SessionLocal, Base
from app.infrastructure.wedding_database import SessionLocal as wedding_SessionLocal
import app.services.wedding_service as wedding_service


Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_main_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_wedding_db():
    db = wedding_SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="./static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
# Routes
#


@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")


@app.get("/version")
def get_version():
    return "0.0.1"


@app.get("/wedding/faq", tags=["wedding"])
def get_all_faqs(db: Session = Depends(get_wedding_db)) -> List[Faq]:
    faqs = wedding_service.get_faqs(db)
    print(faqs)
    return faqs


@app.get("/wedding/faq/{faq_id}", tags=["wedding"])
def get_faq_by_id(faq_id: int, db: Session = Depends(get_wedding_db)) -> Faq:
    faq = wedding_service.get_faq_by_id(db, faq_id)
    if faq is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return faq
