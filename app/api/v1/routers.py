from fastapi import APIRouter

from app.api.v1.endpoints import authentication

router = APIRouter()

router.include_router(authentication.router, prefix="/auth", tags=["authentication"])