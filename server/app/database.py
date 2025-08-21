"""Database setup and models"""
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import Settings

settings = Settings()
Base = declarative_base()

class EarningsCall(Base):
    __tablename__ = "earnings_calls"
    
    id = Column(String, primary_key=True)
    ticker = Column(String, index=True, nullable=False)
    period = Column(String, nullable=False)
    report_time = Column(DateTime, default=datetime.utcnow)
    
    # Data
    provenance = Column(JSON)
    transcript_raw = Column(Text)
    digest = Column(JSON)
    tier_a_bullets = Column(JSON)
    tier_b_summary = Column(Text)
    tier_c_expert = Column(JSON)
    facts = Column(JSON)
    risks = Column(JSON)
    sentiment = Column(JSON)
    qa_highlights = Column(JSON)
    price_windows = Column(JSON)
    charts = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

async def init_db():
    """Initialize database tables"""
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    """Get database session"""
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
