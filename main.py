from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi.staticfiles import StaticFiles

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend
from src.pages.router import router as router_pages
from src.chat.router import router as chat_router

from src.operations.router import router as router_operation

app = FastAPI(
    title="Trading App"
)

app.include_router(
    router_pages,
)
app.include_router(chat_router)

app.mount("/static", StaticFiles(directory='src/static'), name='static')

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
