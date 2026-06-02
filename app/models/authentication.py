from pydantic import BaseModel

class Login(BaseModel):
    identifier: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    refresh_token: str