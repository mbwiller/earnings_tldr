"""
Yahoo Finance Data Provider for EarningsCall-TLDR
Handles fetching market data from Yahoo Finance
"""

import yfinance as yf
from typing import Dict, Any, Optional, List
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class YahooFinanceProvider:
    """Yahoo Finance data provider"""
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_info(self, ticker: str) -> Dict[str, Any]:
        """Get basic stock information"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'ticker': ticker.upper(),
                'company_name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'current_price': info.get('currentPrice', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0)
            }
        except Exception as e:
            logger.error(f"Error fetching stock info for {ticker}: {e}")
            return {}
    
    def get_historical_data(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """Get historical price data"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                return {}
            
            # Calculate key metrics
            current_price = hist['Close'].iloc[-1]
            price_1m_ago = hist['Close'].iloc[-22] if len(hist) >= 22 else hist['Close'].iloc[0]
            price_3m_ago = hist['Close'].iloc[-66] if len(hist) >= 66 else hist['Close'].iloc[0]
            price_1y_ago = hist['Close'].iloc[0]
            
            return {
                'ticker': ticker.upper(),
                'current_price': current_price,
                'price_changes': {
                    '1m': ((current_price - price_1m_ago) / price_1m_ago) * 100,
                    '3m': ((current_price - price_3m_ago) / price_3m_ago) * 100,
                    '1y': ((current_price - price_1y_ago) / price_1y_ago) * 100
                },
                'volume_avg_30d': hist['Volume'].tail(30).mean(),
                'volatility_30d': hist['Close'].tail(30).pct_change().std() * 100,
                'high_52w': hist['High'].max(),
                'low_52w': hist['Low'].min(),
                'data_points': len(hist)
            }
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {e}")
            return {}
    
    def get_earnings_data(self, ticker: str) -> Dict[str, Any]:
        """Get earnings data"""
        try:
            stock = yf.Ticker(ticker)
            earnings = stock.earnings
            
            if earnings is None or earnings.empty:
                return {}
            
            # Get recent earnings
            recent_earnings = earnings.tail(4)
            
            return {
                'ticker': ticker.upper(),
                'recent_earnings': recent_earnings.to_dict('records'),
                'earnings_growth': self._calculate_earnings_growth(recent_earnings),
                'next_earnings_date': stock.calendar.iloc[0]['Earnings Date'] if hasattr(stock, 'calendar') and not stock.calendar.empty else None
            }
        except Exception as e:
            logger.error(f"Error fetching earnings data for {ticker}: {e}")
            return {}
    
    def get_financials(self, ticker: str) -> Dict[str, Any]:
        """Get financial statements"""
        try:
            stock = yf.Ticker(ticker)
            
            # Get financial statements
            income_stmt = stock.financials
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow
            
            return {
                'ticker': ticker.upper(),
                'income_statement': income_stmt.to_dict() if income_stmt is not None else {},
                'balance_sheet': balance_sheet.to_dict() if balance_sheet is not None else {},
                'cash_flow': cash_flow.to_dict() if cash_flow is not None else {},
                'key_metrics': self._extract_key_metrics(income_stmt, balance_sheet, cash_flow)
            }
        except Exception as e:
            logger.error(f"Error fetching financials for {ticker}: {e}")
            return {}
    
    def get_analyst_recommendations(self, ticker: str) -> Dict[str, Any]:
        """Get analyst recommendations"""
        try:
            stock = yf.Ticker(ticker)
            recommendations = stock.recommendations
            
            if recommendations is None or recommendations.empty:
                return {}
            
            # Get recent recommendations
            recent_recs = recommendations.tail(10)
            
            return {
                'ticker': ticker.upper(),
                'recommendations': recent_recs.to_dict('records'),
                'consensus': self._calculate_consensus(recent_recs)
            }
        except Exception as e:
            logger.error(f"Error fetching analyst recommendations for {ticker}: {e}")
            return {}
    
    def get_comprehensive_data(self, ticker: str) -> Dict[str, Any]:
        """Get comprehensive data for a ticker"""
        return {
            'basic_info': self.get_stock_info(ticker),
            'historical_data': self.get_historical_data(ticker),
            'earnings_data': self.get_earnings_data(ticker),
            'financials': self.get_financials(ticker),
            'analyst_recommendations': self.get_analyst_recommendations(ticker)
        }
    
    def _calculate_earnings_growth(self, earnings_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate earnings growth metrics"""
        if len(earnings_df) < 2:
            return {}
        
        try:
            recent_eps = earnings_df['Earnings'].iloc[-1]
            previous_eps = earnings_df['Earnings'].iloc[-2]
            
            growth = ((recent_eps - previous_eps) / abs(previous_eps)) * 100 if previous_eps != 0 else 0
            
            return {
                'quarter_over_quarter': growth,
                'year_over_year': 0  # Would need more data for YoY
            }
        except Exception as e:
            logger.error(f"Error calculating earnings growth: {e}")
            return {}
    
    def _extract_key_metrics(self, income_stmt: pd.DataFrame, balance_sheet: pd.DataFrame, cash_flow: pd.DataFrame) -> Dict[str, Any]:
        """Extract key financial metrics"""
        metrics = {}
        
        try:
            if income_stmt is not None and not income_stmt.empty:
                # Revenue
                if 'Total Revenue' in income_stmt.index:
                    metrics['revenue'] = income_stmt.loc['Total Revenue'].iloc[0]
                
                # Net Income
                if 'Net Income' in income_stmt.index:
                    metrics['net_income'] = income_stmt.loc['Net Income'].iloc[0]
                
                # Gross Margin
                if 'Total Revenue' in income_stmt.index and 'Cost Of Revenue' in income_stmt.index:
                    revenue = income_stmt.loc['Total Revenue'].iloc[0]
                    cost = income_stmt.loc['Cost Of Revenue'].iloc[0]
                    if revenue > 0:
                        metrics['gross_margin'] = ((revenue - cost) / revenue) * 100
            
            if balance_sheet is not None and not balance_sheet.empty:
                # Total Assets
                if 'Total Assets' in balance_sheet.index:
                    metrics['total_assets'] = balance_sheet.loc['Total Assets'].iloc[0]
                
                # Total Debt
                if 'Total Debt' in balance_sheet.index:
                    metrics['total_debt'] = balance_sheet.loc['Total Debt'].iloc[0]
        
        except Exception as e:
            logger.error(f"Error extracting key metrics: {e}")
        
        return metrics
    
    def _calculate_consensus(self, recommendations_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate consensus from analyst recommendations"""
        try:
            # Count recommendations by type
            rec_counts = recommendations_df['To Grade'].value_counts()
            
            # Calculate average price target
            if 'Price Target' in recommendations_df.columns:
                avg_target = recommendations_df['Price Target'].mean()
            else:
                avg_target = None
            
            return {
                'recommendation_counts': rec_counts.to_dict(),
                'average_price_target': avg_target,
                'total_analysts': len(recommendations_df)
            }
        except Exception as e:
            logger.error(f"Error calculating consensus: {e}")
            return {}
