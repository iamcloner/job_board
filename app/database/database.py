from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings import settings
from app.database.indexes import indexes

client = AsyncIOMotorClient(
    settings.MONGODB_URI
)

db = client[settings.MONGODB_DATABASE]

async def startup():
    for collection,fields in indexes.items():
        for field,index in fields:
            try:
                await db[collection].create_index(field,**index)
            except Exception as e:
                if "already exists" in str(e):
                    print(f"{collection}:{field} index already exists({e})")
                else:
                    print(f"Failed to create index.({e}")
