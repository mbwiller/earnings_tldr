"""Process API endpoints"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def process_root():
    return {"endpoint": "process", "status": "ready"}
