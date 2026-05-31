from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = 'mongodb://localhost:27017'
    MONGODB_DATABASE: str = 'job_board'

    JWT_SECRET_KEY: str = 'YOUR_JWT_SECRET_KEY'
    JWT_ACCESS_EXP: int = 120
    JWT_REFRESH_EXP: int = 43200

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()