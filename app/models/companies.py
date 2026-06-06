from datetime import datetime, timezone
from typing import Literal

from bson import ObjectId
from pydantic import BaseModel, Field


class CreateCompany(BaseModel):
    name:str
    description:str
    website:str|None = None
    location:str|None = None
    logo_url:str|None = None
    banner_url:str|None = None
    employee_count:Literal["1-10","10-100","100-1000","+1000"] = "1-10"


class Company(CreateCompany):
    is_active:bool = True
    created_at:datetime = Field(default_factory=lambda :datetime.now(tz=timezone.utc))
    updated_at:datetime = Field(default_factory=lambda :datetime.now(tz=timezone.utc))
    owner_id:ObjectId
    class Config:
        arbitrary_types_allowed = True

class CompanyShow(Company):
    id:str
    owner_id:str