"""Config API endpoints"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def config_root():
    return {"endpoint": "config", "status": "ready"}
