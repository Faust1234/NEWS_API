import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.aiohttpclient import AiohttpClient
from app.core.config import settings
from app.v1.api import api_router
from app.core.system import router


async def on_start_up() -> None:
    logger.info("AiohttpClient starts")
    AiohttpClient.get_aiohttp_client()


async def on_shutdown() -> None:
    logger.info("AiohttpClient closed")
    await AiohttpClient.close_aiohttp_client()


def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME, on_startup=[on_start_up], on_shutdown=[on_shutdown]
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(api_router, prefix=settings.API_V1_STR)
    _app.include_router(router)
    return _app

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
