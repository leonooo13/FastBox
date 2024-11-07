from fastapi import FastAPI, Request, Form, HTTPException
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

# 设置模板目录
templates = Jinja2Templates(directory="templates/user")

# 创建路由器
router = APIRouter()


# 用户页面 GET 请求
@router.get("/user")
def user_page(request: Request):
    return templates.TemplateResponse("user.html", {"request": request, "a": "我是失败"})


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_post(username: str = Form(...), password: str = Form(...)):
    # 注册逻辑：检查用户是否已存在
    if username == "admin":
        raise HTTPException(status_code=400, detail="用户名已存在")
    return RedirectResponse(url="/", status_code=303)


# 登录页面 GET 请求
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 登录表单提交 POST 请求
@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    print("request")
    print(username)
    print(password)
    if username == "admin" and password == "admin":
        return RedirectResponse(url='/', status_code=303)  # 用 GET 请求访问 /index
    error_msg = "失败"
    print(error_msg)
    return templates.TemplateResponse(request=request, name="login.html",context={"error_message":error_msg})
