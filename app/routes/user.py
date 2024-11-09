from datetime import timedelta
from fastapi import FastAPI, Request, Form, HTTPException, Depends, Response
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from app.core.config import settings
from app.routes.deps import SessionDep, get_user_register, CurrentUser, get_current_user
from app.core import crud, security
from app.schemas.user import UserRegister, Token

# 设置模板目录

templates = Jinja2Templates('templates/user')

# 创建路由器
router = APIRouter()


# 用户页面 GET 请求
@router.get("/manage_user")
async def user_page(request: Request, session: SessionDep, current_user: CurrentUser):
    if current_user:
        users = crud.get_all_users(session)
        return templates.TemplateResponse("manage.html", {"request": request, "users": users, "token": 1})
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
        return templates.TemplateResponse(request=request, name="login.html", context={"error_message": e})


@router.post("/logout")
def logout(request: Request, response: Response, current_user: CurrentUser):
    if current_user:
        # 清除存储在 cookie 中的 'token'
        response.delete_cookie('token')
        # 设置重定向
        return RedirectResponse(url="/", status_code=303)
    return RedirectResponse(url="/", status_code=303)


@router.post("/delete_user/{user_id}")
async def delete_user(request: Request, user_id: int, session: SessionDep, current_user: CurrentUser):
    # 调用你的 CRUD 函数删除用户
    if not current_user:
        return RedirectResponse(url="/", status_code=303)
    user = crud.get_user(session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(session, user_id=user_id)
    return RedirectResponse(url="/users", status_code=303)


@router.get("/edit_user/{user_id}", name="edit_user")
async def edit_user(request: Request, user_id: int, session: SessionDep, current_user: CurrentUser):
    if not current_user:
        return RedirectResponse(url="/", status_code=303)
    user = crud.get_user(session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(request=request, name="edit_user.html", context={"user": user})


@router.post("/update_user/{user_id}", name="update_user")
def update_user(user_id: int, current_user: CurrentUser, session: SessionDep,
                name: str = Form(),
                email: str = Form()):
    if not current_user:
        return RedirectResponse(url="/", status_code=303)
    user = crud.get_user(session, user_id=user_id)
    crud.update_user(session, user_id=user_id, name=name, email=email)
    return RedirectResponse(url="/manage_user", status_code=303)
@router.get("/me")
def get_me(request: Request, session: SessionDep, current_user: CurrentUser):
    if not current_user:
        return RedirectResponse(url="/", status_code=303)
    current_user = crud.get_user(session, user_id=current_user.id)
    return templates.TemplateResponse(request=request, name="me.html", context={"user": current_user})
