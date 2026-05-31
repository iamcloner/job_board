
from app.core.utils import PasswordUtils, JWTUtils
from app.models.authentication import JWTLogin
from app.models.users import User, UserCreate, UserShow, UserFind, UserLogin
from app.database.database import db

async def create_user(user_info:UserCreate):
    user = User(**user_info.model_dump(),active=True)
    user.password = PasswordUtils.hash(user_info.password)
    user_res = await db.users.insert_one(user.model_dump())
    return UserShow(**user.model_dump(),id=str(user_res.inserted_id))

async def login_user(user_info:UserLogin) -> JWTLogin:
    user = await db.users.find_one({"username":user_info.username})
    if not user:
        user = await db.users.find_one({"email":user_info.username})
    if not user:
        raise RuntimeError('User not found')
    if not PasswordUtils.verify(user_info.password, user['password']):
        raise RuntimeError('Wrong password')
    access_token = JWTUtils.encode(user['_id'])
    refresh_token = JWTUtils.encode(user['_id'],'refresh_token')
    return JWTLogin(access_token=access_token,refresh_token=refresh_token)

