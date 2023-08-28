import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from controllers.weddingController import buildWeddingEndpoints

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")


@app.get("/version")
def get_version():
    return "0.0.1"


buildWeddingEndpoints(app)
