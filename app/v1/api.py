from fastapi import APIRouter

from app.v1.endpoint import new_endpoint

api_router = APIRouter()
api_router.include_router(new_endpoint.router, tags=["news api"])
