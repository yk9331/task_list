from fastapi import FastAPI

from src.routers.api import api_router

app = FastAPI()

app.include_router(api_router)
