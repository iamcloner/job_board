from datetime import datetime, timezone, timedelta
from typing import Literal

from bson import ObjectId
from passlib.context import CryptContext
from jose import jwt

from app.core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordUtils:
    @staticmethod
    def hash(password:str) -> str:
        return pwd_context.hash(password)
    @staticmethod
    def verify(password:str,hashed_password:str) -> bool:
        return pwd_context.verify(password,hashed_password)

class JWTUtils:
    @staticmethod
    def decode(token:str,token_type:Literal["access_token","refresh_token"]="access_token") -> ObjectId:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        if payload["type"] != token_type:
            raise RuntimeError(f"Invalid token type: {token_type}")
        return ObjectId(payload["sub"])
    @staticmethod
    def encode(user_id:ObjectId,token_type:Literal["access_token","refresh_token"]="access_token") -> str:
        init_time = datetime.now(timezone.utc)
        exp = timedelta(minutes=settings.JWT_ACCESS_EXP) if token_type == "access_token" else timedelta(minutes=settings.JWT_REFRESH_EXP)
        jwt_payload = {
            "iat": init_time,
            "sub": str(user_id),
            "type":token_type,
            "nbf": init_time,
            "exp": init_time + exp,
        }
        return jwt.encode(jwt_payload, settings.JWT_SECRET_KEY, algorithm="HS256")

class ResponseUtils:
    @staticmethod
    def ObjectId_Serializer(obj:dict,field_name:str,response_field_name:str|None=None) -> dict:
        if field_name not in obj:
            raise IndexError(f"{field_name} is not exist")
        obj[response_field_name if response_field_name else field_name] = str(obj.pop(field_name))
        return obj