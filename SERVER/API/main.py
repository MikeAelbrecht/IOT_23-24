# File of the webserver
# The webserver will list the database entries
# In the CMD run python3 -m uvicorn SERVER.API.main:app --reload (from the IOT_2023 folder)

import subprocess
from typing import Union

try:
    from fastapi import FastAPI, Request
except ModuleNotFoundError:
    subprocess.run(["pip", "install", "fastapi"])
    from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
