"""
Enhanced Multi-Stock Price Streaming
Supports streaming prices for multiple stocks simultaneously
"""
import yfinance as yf
import time
import pandas as pd
from typing import List, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from src.utils.helpers import save_csv
from src.utils.logger import get_logger
from src.utils.config import Config

logger = get_logger(__name__)


def fetch_stock_price(symbol: str, period: str = "1d") -> pd.DataFrame:
    """Fetch latest price data for a single stock"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval="1m")
        
        if data.empty:
            logger.warning(f"No data available for {symbol}")
            return pd.DataFrame()
        
        # Add symbol column
        data = data.reset_index()
        data['symbol'] = symbol
        data['scraped_at'] = datetime.now().isoformat()
        
        return data
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return pd.DataFrame()


def stream_prices(symbols: Optional[List[str]] = None, interval: int = 60, save_individual: bool = True):
    """
    Stream prices for multiple stocks
    
    Args:
        symbols: List of stock symbols to stream. If None, uses Config.STOCKS
        interval: Update interval in seconds
        save_individual: Whether to save individual stock files
    """
    symbols = symbols or Config.STOCKS
    logger.info(f"Starting price streaming for {len(symbols)} stocks: {symbols}")
    
    all_prices = []
    
    while True:
        try:
            # Fetch prices for all stocks
            with ThreadPoolExecutor(max_workers=min(len(symbols), 5)) as executor:
                futures = {executor.submit(fetch_stock_price, symbol): symbol for symbol in symbols}
                
                current_prices = []
                for future in futures:
                    symbol = futures[future]
                    try:
                        df = future.result(timeout=30)
                        if not df.empty:
                            current_prices.append(df)
                            if save_individual:
                                # Save individual stock price
                                latest = df.tail(1)
                                save_csv(latest, f"data/raw/prices/latest_price_{symbol}.csv")
                    except Exception as e:
                        logger.error(f"Error fetching {symbol}: {e}")
                        continue
            
            if current_prices:
                # Combine all prices
                combined_df = pd.concat(current_prices, ignore_index=True)
                
                # Save combined latest prices
                latest_prices = combined_df.groupby('symbol').tail(1)
                save_csv(latest_prices, "data/raw/prices/latest_price.csv")
                
                # Append to historical data
                all_prices.append(combined_df)
                
                # Save historical prices (keep last 1000 records per stock)
                if len(all_prices) > 0:
                    historical = pd.concat(all_prices, ignore_index=True)
                    historical = historical.sort_values(['symbol', 'Datetime']).groupby('symbol').tail(1000)
                    save_csv(historical, "data/raw/prices/historical_prices.csv")
                
                logger.info(f"Updated prices for {len(current_prices)} stocks at {time.strftime('%H:%M:%S')}")
                print(f"✓ Updated prices for {len(current_prices)} stocks at {time.strftime('%H:%M:%S')}")
            else:
                logger.warning("No price data fetched")
            
            time.sleep(interval)
            
        except KeyboardInterrupt:
            logger.info("Price streaming stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in streaming loop: {e}")
            time.sleep(interval)


if __name__ == "__main__":
    # Stream prices for all configured stocks
    stream_prices(symbols=Config.STOCKS, interval=60)
