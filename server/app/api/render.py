"""Render API endpoints"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def render_root():
    return {"endpoint": "render", "status": "ready"}
