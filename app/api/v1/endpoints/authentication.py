from fastapi import APIRouter

from app.models.users import UserShow, UserCreate
from app.services.users import create_user

router = APIRouter()

@router.post("/register",response_model=UserShow)
async def register(user_info:UserCreate):
    return await create_user(user_info)