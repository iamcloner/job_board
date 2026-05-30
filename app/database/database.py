from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings import settings

client = AsyncIOMotorClient(
    settings.MONGODB_URI
)

db = client[settings.MONGODB_DATABASE]