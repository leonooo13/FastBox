from datetime import timedelta

from fastapi import FastAPI, Request, Form, HTTPException, Depends, Response
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

from app.core.config import settings
from app.routes.deps import SessionDep, get_user_register, CurrentUser
from app.core import crud, security
from app.schemas.user import UserRegister, Token

# 设置模板目录
templates = Jinja2Templates(directory="templates/user")

# 创建路由器
router = APIRouter()


# 用户页面 GET 请求
@router.get("/manage_user")
async def user_page(request: Request, session: SessionDep, current_user: CurrentUser):
    if current_user:
        users = crud.get_all_users(session)
        return templates.TemplateResponse("user.html", {"request": request, "users": users, "token":1})
    return RedirectResponse("/")


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(request: Request, session: SessionDep, user_reg: UserRegister = Depends(get_user_register)):
    # 注册逻辑：检查用户是否已存在

    try:
        user_reg.validate_password_match()
        crud.create_user(user_reg, session)
    except Exception as e:
        return templates.TemplateResponse(request=request, name="register.html", context={"error": e})
    return RedirectResponse(url="/", status_code=303)


# 登录页面 GET 请求
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


# 登录表单提交 POST 请求
@router.post("/login")
async def login(request: Request, session: SessionDep, username: str = Form(...), password: str = Form(...)):
    try:
        user = crud.authenticate(
            session=session, username=username, password=password
        )
        if not user:
            raise ValueError("用户不存在")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            user.id, expires_delta=access_token_expires)
        user_token = Token(access_token=access_token)
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="token",
            value=f"{user_token.token_type} {user_token.access_token}",
            httponly=True,
            secure=True,  # 在生产环境中开启
            samesite="lax"  # 防止 CSRF
        )
        return response
    except Exception as e:
        print(e)
        return templates.TemplateResponse(request=request, name="login.html", context={"error_message": e})


@router.post("/logout")
def logout(request: Request, response: Response, current_user: CurrentUser):
    # 清除存储在 cookie 中的 'token'
    if current_user:
        response.headers['Location'] = '/'  # 指定重定向的 URL
        response.status_code = 303  # 设置 HTTP 状态码为 303, 表示重定向
        response.delete_cookie('token')
        # return RedirectResponse(url="/", status_code=303)
        return response
