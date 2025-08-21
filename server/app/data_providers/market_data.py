"""
Market Data Provider for EarningsCall-TLDR
Orchestrates all market data sources
"""

from typing import Dict, Any, Optional
from .yahoo_finance import YahooFinanceProvider
from .alpha_vantage import AlphaVantageProvider
import logging

logger = logging.getLogger(__name__)

class MarketDataProvider:
    """Main market data provider that orchestrates all data sources"""
    
    def __init__(self, yahoo_enabled: bool = True, alpha_vantage_enabled: bool = False):
        self.yahoo_provider = YahooFinanceProvider() if yahoo_enabled else None
        self.alpha_vantage_provider = AlphaVantageProvider() if alpha_vantage_enabled else None
        
    def get_comprehensive_market_data(self, ticker: str) -> Dict[str, Any]:
        """Get comprehensive market data from all available sources"""
        data = {
            'ticker': ticker.upper(),
            'sources': [],
            'data': {}
        }
        
        # Get data from Yahoo Finance
        if self.yahoo_provider:
            try:
                yahoo_data = self.yahoo_provider.get_comprehensive_data(ticker)
                data['data']['yahoo_finance'] = yahoo_data
                data['sources'].append('yahoo_finance')
            except Exception as e:
                logger.error(f"Error fetching Yahoo Finance data: {e}")
        
        # Get data from Alpha Vantage (when implemented)
        if self.alpha_vantage_provider:
            try:
                alpha_data = self.alpha_vantage_provider.get_stock_data(ticker)
                data['data']['alpha_vantage'] = alpha_data
                data['sources'].append('alpha_vantage')
            except Exception as e:
                logger.error(f"Error fetching Alpha Vantage data: {e}")
        
        return data
    
    def get_stock_price_data(self, ticker: str) -> Dict[str, Any]:
        """Get current stock price and basic info"""
        if self.yahoo_provider:
            return self.yahoo_provider.get_stock_info(ticker)
        return {}
    
    def get_historical_price_data(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """Get historical price data"""
        if self.yahoo_provider:
            return self.yahoo_provider.get_historical_data(ticker, period)
        return {}
    
    def get_earnings_data(self, ticker: str) -> Dict[str, Any]:
        """Get earnings data"""
        if self.yahoo_provider:
            return self.yahoo_provider.get_earnings_data(ticker)
        return {}
