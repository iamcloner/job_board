from app.models.users import User, UserCreate, UserShow
from app.database.database import db


async def create_user(user_info:UserCreate):
    user = User(**user_info.model_dump(),active=True)
    user_res = await db.users.insert_one(user.model_dump())
    return UserShow(**user.model_dump(),id=str(user_res.inserted_id))