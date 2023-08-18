from app.api.api_v1.endpoints import login, users, messages
from fastapi.routing import APIRouter

api_router = APIRouter()

api_router.include_router(router=login.router, tags=["Login"])
api_router.include_router(router=users.router, tags=["Users"], prefix="/users")
api_router.include_router(router=messages.router, tags=["Messages"], prefix="/messages")
