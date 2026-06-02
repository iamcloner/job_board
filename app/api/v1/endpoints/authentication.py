from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.errors import DuplicateKeyError

from app.models.authentication import Login, Token
from app.models.users import UserShow, UserCreate
from app.services.users import create_user, login_user,authenticate_user

router = APIRouter()

@router.post("/register",response_model=UserShow)
async def register(user_info:UserCreate):
    try:
        return await create_user(user_info)
    except DuplicateKeyError as e:
        if e.details['code'] == 11000:
            if "email_" in str(e):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already exists")
            if "username_" in str(e):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal Server Error")

@router.post("/login",response_model=Token)
async def login(user_info:OAuth2PasswordRequestForm = Depends()):
    try:
        return await login_user(Login(identifier=user_info.username,password=user_info.password))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal Server Error")


@router.get("/me",response_model=UserShow)
async def me(current_user = Depends(authenticate_user)) -> UserShow:
    return current_user
