from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory="/code/app/static"), name="static")

@app.get("/")
def read_root():
    return RedirectResponse(url='/static/index.html')

