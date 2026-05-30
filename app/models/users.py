from datetime import datetime, timezone

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(UserLogin):
    name: str
    email: str

class User(UserCreate):
    active: bool
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    class Config:
        arbitrary_types_allowed = True

class UserShow(User):
    password:str = "*******"

class UserEdit(UserCreate):
    pass

class UserPartialEdit(BaseModel):
    name: str | None
    username: str | None
    email: EmailStr | None
    password: str | None