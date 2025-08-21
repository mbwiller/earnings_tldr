"""Ingest API endpoints"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import json
import logging
from pathlib import Path
import aiofiles

from app.nlp.processor import TranscriptProcessor
from app.nlp.rag_engine import RAGEngine
from app.data_providers.market_data import MarketDataProvider
from app.reporting.pdf_generator import PDFGenerator
from app.config import Settings

logger = logging.getLogger(__name__)
settings = Settings()

router = APIRouter()

@router.get("/")
async def ingest_root():
    return {"endpoint": "ingest", "status": "ready"}

@router.post("/")
async def ingest_file(
    file: Optional[UploadFile] = File(None),
    ticker: Optional[str] = Form(None),
    period: Optional[str] = Form(None)
):
    """Ingest and analyze earnings call transcript"""
    
    try:
        # Initialize components
        processor = TranscriptProcessor(
            max_chunk_size=settings.MAX_CHUNK_SIZE,
            min_chunk_size=settings.MIN_CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        rag_engine = RAGEngine(settings.OPENAI_API_KEY)
        market_data_provider = MarketDataProvider(
            yahoo_enabled=settings.YAHOO_FINANCE_ENABLED,
            alpha_vantage_enabled=settings.ALPHA_VANTAGE_ENABLED
        )
        
        # Process transcript
        transcript_text = ""
        if file:
            # Read uploaded file
            content = await file.read()
            transcript_text = content.decode('utf-8')
        else:
            # Use sample transcript for testing
            sample_path = Path("../../samples/AAPL_Q2_FY2025_transcript.txt")
            if sample_path.exists():
                async with aiofiles.open(sample_path, 'r') as f:
                    transcript_text = await f.read()
            else:
                # Fallback to mock data
                transcript_text = "Sample earnings call transcript content..."
        
        # Process transcript
        processed_data = processor.process_transcript(transcript_text)
        
        # Get market data
        market_data = {}
        if ticker:
            market_data = market_data_provider.get_comprehensive_market_data(ticker)
        
        # Analyze using RAG
        analysis_result = rag_engine.analyze_earnings_call(
            processed_data['chunks'], 
            market_data
        )
        
        # Add metadata
        analysis_result.update({
            'id': f"{ticker.upper()}_{period.replace(' ', '_')}" if ticker and period else "analysis_001",
            'ticker': ticker.upper() if ticker else "AAPL",
            'period': period if period else "Q2 FY2025",
            'status': 'completed',
            'metadata': {
                'total_tokens': processed_data['metadata']['total_tokens'],
                'num_chunks': processed_data['metadata']['num_chunks'],
                'processing_time': 'mock_time'
            }
        })
        
        # Generate PDF report
        settings.PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        pdf_generator = PDFGenerator()
        pdf_filename = f"{analysis_result['id']}_report.pdf"
        pdf_path = settings.PDF_OUTPUT_DIR / pdf_filename
        
        try:
            pdf_generator.generate_analysis_report(analysis_result, str(pdf_path))
            analysis_result['pdf_report'] = f"/data/reports/pdf/{pdf_filename}"
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            analysis_result['pdf_report'] = None
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error in ingest_file: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
