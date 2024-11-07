from fastapi import APIRouter

from app.routes import user
from app.routes import main

api_router = APIRouter()

api_router.include_router(main.router, tags=["main"])
api_router.include_router(user.router, tags=["users"])
