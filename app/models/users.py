import datetime

from pydantic import BaseModel
from pydantic.v1 import EmailStr


class UserLogin(BaseModel):
    username: str | EmailStr
    password: str

class UserCreate(UserLogin):
    name: str
    username: str
    email: str

class User(UserCreate):
    active: bool
    created_at: datetime = Field(default_factory=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.datetime.now(tz=datetime.timezone.utc))

class ShowUser(User):
    password:str = "*******"

class UserEdit(UserCreate):
    pass

class UserPartialEdit(BaseModel):
    name: str | None
    username: str | None
    email: EmailStr | None
    password: str | None