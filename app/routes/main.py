from fastapi import FastAPI, Request, Form
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
router = APIRouter()
@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})