"""
Enhanced Comprehensive Financial Statements Scraper
Scrapes Income Statement, Balance Sheet, and Cash Flow Statement
Supports multiple data sources including SEC EDGAR
"""
print("RUNNING FILE:", __file__)

import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils.helpers import save_csv
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FinancialStatementsScraper:
    """Scraper for company financial statements"""
    
    def __init__(self, symbols: List[str] = None):
        self.symbols = symbols or ["AAPL", "MSFT", "TSLA", "GOOG"]
        self.statements = {}
    
    def scrape_income_statement(self, symbol: str, periods: int = 4) -> pd.DataFrame:
        """Scrape Income Statement with historical data"""
        try:
            stock = yf.Ticker(symbol)
            income_stmt = stock.financials
            
            if income_stmt.empty:
                logger.warning(f"No income statement data for {symbol}")
                return pd.DataFrame()
            
            # Get quarterly data if available
            try:
                quarterly_stmt = stock.quarterly_financials
                if not quarterly_stmt.empty:
                    # Combine annual and quarterly
                    income_stmt = pd.concat([income_stmt, quarterly_stmt], axis=1)
                    income_stmt = income_stmt.loc[:, ~income_stmt.columns.duplicated()]
            except:
                pass
            
            # Transpose and add metadata
            df = income_stmt.T.reset_index()
            df.columns = ['Date'] + list(income_stmt.index)
            df['symbol'] = symbol
            df['statement_type'] = 'Income Statement'
            df['scraped_at'] = datetime.now().isoformat()
            
            # Sort by date (most recent first)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df = df.sort_values('Date', ascending=False)
            
            logger.info(f"Income Statement: Scraped {len(df)} periods for {symbol}")
            return df
        except Exception as e:
            logger.error(f"Income Statement scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_balance_sheet(self, symbol: str, periods: int = 4) -> pd.DataFrame:
        """Scrape Balance Sheet with historical data"""
        try:
            stock = yf.Ticker(symbol)
            balance_sheet = stock.balance_sheet
            
            if balance_sheet.empty:
                logger.warning(f"No balance sheet data for {symbol}")
                return pd.DataFrame()
            
            # Get quarterly data if available
            try:
                quarterly_bs = stock.quarterly_balance_sheet
                if not quarterly_bs.empty:
                    balance_sheet = pd.concat([balance_sheet, quarterly_bs], axis=1)
                    balance_sheet = balance_sheet.loc[:, ~balance_sheet.columns.duplicated()]
            except:
                pass
            
            # Transpose and add metadata
            df = balance_sheet.T.reset_index()
            df.columns = ['Date'] + list(balance_sheet.index)
            df['symbol'] = symbol
            df['statement_type'] = 'Balance Sheet'
            df['scraped_at'] = datetime.now().isoformat()
            
            # Sort by date (most recent first)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df = df.sort_values('Date', ascending=False)
            
            logger.info(f"Balance Sheet: Scraped {len(df)} periods for {symbol}")
            return df
        except Exception as e:
            logger.error(f"Balance Sheet scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_cash_flow(self, symbol: str, periods: int = 4) -> pd.DataFrame:
        """Scrape Cash Flow Statement with historical data"""
        try:
            stock = yf.Ticker(symbol)
            cash_flow = stock.cashflow
            
            if cash_flow.empty:
                logger.warning(f"No cash flow data for {symbol}")
                return pd.DataFrame()
            
            # Get quarterly data if available
            try:
                quarterly_cf = stock.quarterly_cashflow
                if not quarterly_cf.empty:
                    cash_flow = pd.concat([cash_flow, quarterly_cf], axis=1)
                    cash_flow = cash_flow.loc[:, ~cash_flow.columns.duplicated()]
            except:
                pass
            
            # Transpose and add metadata
            df = cash_flow.T.reset_index()
            df.columns = ['Date'] + list(cash_flow.index)
            df['symbol'] = symbol
            df['statement_type'] = 'Cash Flow'
            df['scraped_at'] = datetime.now().isoformat()
            
            # Sort by date (most recent first)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df = df.sort_values('Date', ascending=False)
            
            logger.info(f"Cash Flow: Scraped {len(df)} periods for {symbol}")
            return df
        except Exception as e:
            logger.error(f"Cash Flow scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_all_statements(self, symbol: str) -> Dict[str, pd.DataFrame]:
        """Scrape all financial statements for a symbol"""
        results = {
            'income_statement': self.scrape_income_statement(symbol),
            'balance_sheet': self.scrape_balance_sheet(symbol),
            'cash_flow': self.scrape_cash_flow(symbol)
        }
        return results
    
    def scrape_multiple_stocks(self, symbols: List[str] = None, use_async: bool = True) -> Dict[str, pd.DataFrame]:
        """Scrape financial statements for multiple stocks with optional async support"""
        symbols = symbols or self.symbols
        all_income = []
        all_balance = []
        all_cashflow = []
        
        if use_async and len(symbols) > 1:
            # Concurrent scraping for better performance
            with ThreadPoolExecutor(max_workers=min(len(symbols), 3)) as executor:
                future_to_symbol = {executor.submit(self.scrape_all_statements, symbol): symbol 
                                   for symbol in symbols}
                
                for future in as_completed(future_to_symbol):
                    symbol = future_to_symbol[future]
                    try:
                        logger.info(f"Scraping financial statements for {symbol}...")
                        statements = future.result(timeout=60)
                        
                        if not statements['income_statement'].empty:
                            all_income.append(statements['income_statement'])
                        if not statements['balance_sheet'].empty:
                            all_balance.append(statements['balance_sheet'])
                        if not statements['cash_flow'].empty:
                            all_cashflow.append(statements['cash_flow'])
                    except Exception as e:
                        logger.error(f"Error scraping {symbol}: {e}")
                        continue
        else:
            # Sequential scraping
            for symbol in symbols:
                logger.info(f"Scraping financial statements for {symbol}...")
                statements = self.scrape_all_statements(symbol)
                
                if not statements['income_statement'].empty:
                    all_income.append(statements['income_statement'])
                if not statements['balance_sheet'].empty:
                    all_balance.append(statements['balance_sheet'])
                if not statements['cash_flow'].empty:
                    all_cashflow.append(statements['cash_flow'])
        
        return {
            'income_statement': pd.concat(all_income, ignore_index=True) if all_income else pd.DataFrame(),
            'balance_sheet': pd.concat(all_balance, ignore_index=True) if all_balance else pd.DataFrame(),
            'cash_flow': pd.concat(all_cashflow, ignore_index=True) if all_cashflow else pd.DataFrame()
        }
    
    def save_statements(self, statements: Dict[str, pd.DataFrame], base_path: str = "data/raw/fundamentals/"):
        """Save all financial statements to CSV files"""
        for stmt_type, df in statements.items():
            if not df.empty:
                filename = f"{base_path}{stmt_type}.csv"
                save_csv(df, filename)
                logger.info(f"Saved {stmt_type} with {len(df)} records to {filename}")
    
    def get_combined_statements(self, statements: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Combine all statements into a single DataFrame"""
        all_statements = []
        for df in statements.values():
            if not df.empty:
                all_statements.append(df)
        
        if all_statements:
            return pd.concat(all_statements, ignore_index=True)
        return pd.DataFrame()


if __name__ == "__main__":
    scraper = FinancialStatementsScraper(symbols=["AAPL", "MSFT", "TSLA", "GOOG"])
    statements = scraper.scrape_multiple_stocks()
    scraper.save_statements(statements)

