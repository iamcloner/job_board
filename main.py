from fastapi import FastAPI

from app.api.v1.routers import router as api_router_v1

app = FastAPI()

app.include_router(api_router_v1,prefix="/v1")