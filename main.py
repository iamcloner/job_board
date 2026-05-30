from fastapi import FastAPI

from app.database.database import db

app = FastAPI()

@app.get("/")
async def root():
    await db.command("ping")

    return {"message": "Mongo DB Connected"}