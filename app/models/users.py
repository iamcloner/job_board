from datetime import datetime, timezone

from bson import ObjectId
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
    created_at: datetime = Field(default_factory=lambda :datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda :datetime.now(tz=timezone.utc))
    class Config:
        arbitrary_types_allowed = True

class UserShow(User):
    id:str
    password: str = Field(exclude=True)

class UserEdit(UserCreate):
    pass

class UserPartialEdit(BaseModel):
    name: str | None
    username: str | None
    email: EmailStr | None
    password: str | None