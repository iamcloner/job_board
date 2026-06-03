from fastapi import APIRouter

from app.api.v1.endpoints import authentication, companies

router = APIRouter()

router.include_router(authentication.router, prefix="/auth", tags=["authentication"])
router.include_router(companies.router, prefix="/companies", tags=["companies"])