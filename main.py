from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.main_route import api_router
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)