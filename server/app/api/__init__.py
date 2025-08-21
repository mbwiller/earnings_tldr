from .health import router as health_router
from .ingest import router as ingest_router
from .process import router as process_router
from .render import router as render_router
from .config import router as config_router

__all__ = [
    "health_router",
    "ingest_router", 
    "process_router",
    "render_router",
    "config_router"
]
