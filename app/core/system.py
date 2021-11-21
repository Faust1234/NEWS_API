from fastapi import APIRouter


router = APIRouter()


@router.get("/status", tags=["system"])
async def health_check():
    return {"status": "healthy"}
