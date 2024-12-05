from fastapi import FastAPI, Request, Form, HTTPException, Depends, Response
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from app.routes.deps import SessionDep, get_user_register, CurrentUser, get_current_user
from app.schemas.project import ProjectCreate
from app.core.project.crud import ProjectCrude

# 设置模板目录

templates = Jinja2Templates('templates/project')

# 创建路由器
router = APIRouter()


# 用户页面 GET 请求
@router.get("/projects")
async def get_projects(request: Request, db_session: SessionDep):
    projects = ProjectCrude(db_session).get_all_projects()
    for project in projects:
        project.status = project.status.value
    return templates.TemplateResponse(request=request, name="ProjectManage.html", context={"projects": projects})


@router.get("/add_project")
async def add_project(request: Request):
    return templates.TemplateResponse(request=request, name="AddForm.html", context={})


@router.post("/add_project")
async def add_project(request: Request, db_session: SessionDep):
    form_data = await request.form()
    new_project = ProjectCreate(**form_data)
    ProjectCrude(db_session=db_session).create(project=new_project)
    return RedirectResponse(url="/projects", status_code=303)
