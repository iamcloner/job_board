from pydantic import BaseModel


class JWTLogin(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    refresh_token: str