"""EarningsCall-TLDR Server"""
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.config import Settings
from app.database import init_db
from app.api import health_router, ingest_router, process_router, render_router, config_router

sys.path.insert(0, str(Path(__file__).parent))
settings = Settings()

# Setup templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "app" / "templates"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup"""
    await init_db()
    
    for dir_path in [
        settings.DATA_DIR / "raw",
        settings.DATA_DIR / "processed", 
        settings.DATA_DIR / "cache",
        settings.DATA_DIR / "reports"
    ]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    yield

app = FastAPI(
    title="EarningsCall-TLDR API",
    version="1.0.0",
    description="Intelligent earnings call analysis",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/data", StaticFiles(directory=str(settings.DATA_DIR)), name="data")

# Web routes
@app.get("/")
async def dashboard(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/upload")
async def upload_page(request: Request):
    """Upload page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/search")
async def search_page(request: Request):
    """Search page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/history")
async def history_page(request: Request):
    """History page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

# API routes
app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(ingest_router, prefix="/api/ingest", tags=["ingest"])
app.include_router(process_router, prefix="/api/process", tags=["process"])
app.include_router(render_router, prefix="/api/render", tags=["render"])
app.include_router(config_router, prefix="/api/config", tags=["config"])

# Additional API routes for the web interface
@app.get("/api/search/{ticker}")
async def search_earnings_calls(ticker: str):
    """Search for earnings calls by ticker"""
    # Mock data for now - replace with actual database query
    return {
        "ticker": ticker.upper(),
        "earnings_calls": [
            {
                "id": f"{ticker.upper()}_Q2_2025",
                "ticker": ticker.upper(),
                "period": "Q2 FY2025",
                "report_time": "2025-04-27T16:30:00Z",
                "status": "analyzed"
            }
        ]
    }

@app.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get analysis results by ID"""
    # Mock data for now - replace with actual database query
    return {
        "id": analysis_id,
        "ticker": "AAPL",
        "period": "Q2 FY2025",
        "tier_a_bullets": [
            {
                "text": "Revenue beat expectations by 3%",
                "sentiment": "positive",
                "confidence": 85
            },
            {
                "text": "iPhone sales grew 7% year-over-year",
                "sentiment": "positive", 
                "confidence": 92
            },
            {
                "text": "Services revenue reached all-time high",
                "sentiment": "positive",
                "confidence": 88
            }
        ],
        "tier_b_summary": "Apple reported strong Q2 results with revenue of $97.3 billion, up 5% year-over-year. The company exceeded expectations across all major product categories, with iPhone revenue growing 7% and Services reaching a new record. Gross margins improved to 45.2%, reflecting favorable product mix and operational efficiencies.",
        "tier_c_expert": {
            "metrics": {
                "revenue": "$97.3B (+5% YoY)",
                "eps": "$1.53 (+9% YoY)",
                "gross_margin": "45.2%",
                "services_growth": "12% YoY"
            }
        },
        "facts": [
            {"metric": "Revenue", "value": "$97.3B"},
            {"metric": "EPS", "value": "$1.53"},
            {"metric": "iPhone Revenue", "value": "$51.3B"},
            {"metric": "Services Revenue", "value": "$23.1B"}
        ],
        "risks": [
            {"description": "Supply chain constraints in China"},
            {"description": "Regulatory scrutiny of App Store practices"},
            {"description": "Macroeconomic headwinds affecting consumer spending"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )
