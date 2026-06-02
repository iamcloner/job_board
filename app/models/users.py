from datetime import datetime, timezone

from bson import ObjectId
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str

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
    name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserFind(UserPartialEdit):
    active: bool | None = None