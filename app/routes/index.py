from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.routes.deps import SessionDep, CurrentUser, get_current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def index(request: Request, session: SessionDep, current_user: CurrentUser):
    if current_user:
        username = current_user.name
        return templates.TemplateResponse(request=request, name="index.html",
                                          context={"username": username, "token": 1})
    return RedirectResponse("/login")
