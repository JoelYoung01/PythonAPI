from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.infrastructure.main_database import engine, Base
from app.routers.wedding import build_app as build_wedding_app


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.mount("/static", StaticFiles(directory="app/static"), name="static")


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


# Redirect root to index.html
@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/static/index.html")


# Redirect favicon to static file
@app.get("/favicon.ico", include_in_schema=False)
def read_favicon():
    return RedirectResponse(url="/static/favicon.ico")


app.mount("/wedding", build_wedding_app())
