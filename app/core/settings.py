from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = 'mongodb://localhost:27017'
    MONGODB_DATABASE: str = 'job_board'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()