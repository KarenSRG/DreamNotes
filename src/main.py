from src.config import REDIS_HOST
from src.note.router import router as note_router
from src.user.router import router as user_router

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url(REDIS_HOST, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)

app.include_router(note_router, prefix="/api", tags=["notes"])
app.include_router(user_router, prefix="/api", tags=["user"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the DreamNotesAPI."}
