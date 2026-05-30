from fastapi import FastAPI

from app.api.v1.routers import router as api_router_v1
from app.database.database import startup as db_startup

async def startup(app: FastAPI):
    await db_startup()
    yield
app = FastAPI(lifespan=startup)

app.include_router(api_router_v1,prefix="/v1")

