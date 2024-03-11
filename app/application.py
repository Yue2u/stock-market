from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.auth import router as auth_router
from .routers.user import router as user_router

fastapi_app = FastAPI()

fastapi_app.include_router(auth_router, prefix="/api")
fastapi_app.include_router(user_router, prefix="/api")


fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените "*" на нужные вам домены
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
