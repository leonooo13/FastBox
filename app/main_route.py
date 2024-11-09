from fastapi import APIRouter

from app.routes import user
from app.routes import index
from app.routes import project
api_router = APIRouter()

api_router.include_router(index.router, tags=["main"])
api_router.include_router(user.router, tags=["users"])
api_router.include_router(project.router, tags=["project"])
