from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.utils import PasswordUtils, JWTUtils
from app.models.authentication import Login,Token
from app.models.users import User, UserCreate, UserShow
from app.database.database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

async def create_user(user_info:UserCreate):
    user = User(**user_info.model_dump(),active=True)
    user.password = PasswordUtils.hash(user_info.password)
    user_res = await db.users.insert_one(user.model_dump())
    return UserShow(**user.model_dump(),id=str(user_res.inserted_id))

async def login_user(user_info:Login) -> Token:
    user = await db.users.find_one({"username":user_info.identifier})
    if not user:
        user = await db.users.find_one({"email":user_info.identifier})
    if not user:
        raise RuntimeError('User not found')
    if not PasswordUtils.verify(user_info.password, user['password']):
        raise RuntimeError('Wrong password')
    access_token = JWTUtils.encode(user['_id'])
    refresh_token = JWTUtils.encode(user['_id'],'refresh_token')
    return Token(access_token=access_token,refresh_token=refresh_token)

async def authenticate_user(token = Depends(oauth2_scheme)) -> UserShow:
    try:
        user_id = JWTUtils.decode(token,'access_token')
        user = await db.users.find_one({"_id":user_id})
        if not user or not user['active']:
            raise RuntimeError('User not found')
        return UserShow(**user,id=str(user_id))
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed to authenticate user")