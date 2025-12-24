"""
Enhanced Multi-source news scraper for stock intelligence platform
Supports: Yahoo Finance, Reuters, MarketWatch, Bloomberg, Finviz, Seeking Alpha, CNBC, Benzinga
With async/concurrent scraping capabilities
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.helpers import save_csv
from src.utils.logger import get_logger

logger = get_logger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


class MultiSourceScraper:
    """Scraper for multiple news sources"""
    
    def __init__(self, symbols: List[str] = None):
        self.symbols = symbols or ["AAPL", "MSFT", "TSLA", "GOOG"]
        self.results = []
    
    def scrape_yahoo_finance(self, symbol: str) -> pd.DataFrame:
        """Scrape news from Yahoo Finance"""
        try:
            url = f"https://finance.yahoo.com/quote/{symbol}/news"
            response = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            
            data = []
            # Yahoo Finance news selectors
            for item in soup.select("h3 a, h2 a"):
                headline = item.get_text(strip=True)
                link = item.get("href", "")
                if headline and len(headline) > 10:
                    data.append({
                        "symbol": symbol,
                        "source": "Yahoo Finance",
                        "headline": headline,
                        "url": f"https://finance.yahoo.com{link}" if link.startswith("/") else link,
                        "published_at": datetime.now().isoformat(),
                        "scraped_at": datetime.now().isoformat()
                    })
            
            logger.info(f"Yahoo Finance: Scraped {len(data)} articles for {symbol}")
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Yahoo Finance scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_reuters(self, symbol: str) -> pd.DataFrame:
        """Scrape news from Reuters"""
        try:
            url = f"https://www.reuters.com/companies/{symbol}.OQ"
            response = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            
            data = []
            for item in soup.select("a[data-testid='Link'], h3 a"):
                headline = item.get_text(strip=True)
                link = item.get("href", "")
                if headline and len(headline) > 10:
                    data.append({
                        "symbol": symbol,
                        "source": "Reuters",
                        "headline": headline,
                        "url": f"https://www.reuters.com{link}" if link.startswith("/") else link,
                        "published_at": datetime.now().isoformat(),
                        "scraped_at": datetime.now().isoformat()
                    })
            
            logger.info(f"Reuters: Scraped {len(data)} articles for {symbol}")
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Reuters scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_marketwatch(self, symbol: str) -> pd.DataFrame:
        """Scrape news from MarketWatch"""
        try:
            url = f"https://www.marketwatch.com/investing/stock/{symbol}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            
            data = []
            for item in soup.select("h3 a, .article__headline a"):
                headline = item.get_text(strip=True)
                link = item.get("href", "")
                if headline and len(headline) > 10:
                    data.append({
                        "symbol": symbol,
                        "source": "MarketWatch",
                        "headline": headline,
                        "url": f"https://www.marketwatch.com{link}" if link.startswith("/") else link,
                        "published_at": datetime.now().isoformat(),
                        "scraped_at": datetime.now().isoformat()
                    })
            
            logger.info(f"MarketWatch: Scraped {len(data)} articles for {symbol}")
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"MarketWatch scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_finviz(self, symbol: str) -> pd.DataFrame:
        """Scrape news from Finviz"""
        try:
            url = f"https://finviz.com/quote.ashx?t={symbol}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            
            data = []
            # Finviz news table
            news_table = soup.find("table", {"id": "news-table"})
            if news_table:
                for row in news_table.find_all("tr")[:20]:  # Limit to 20 articles
                    cells = row.find_all("td")
                    if len(cells) >= 2:
                        headline = cells[1].get_text(strip=True)
                        link = cells[1].find("a")
                        url_link = link.get("href", "") if link else ""
                        if headline:
                            data.append({
                                "symbol": symbol,
                                "source": "Finviz",
                                "headline": headline,
                                "url": url_link,
                                "published_at": datetime.now().isoformat(),
                                "scraped_at": datetime.now().isoformat()
                            })
            
            logger.info(f"Finviz: Scraped {len(data)} articles for {symbol}")
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Finviz scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_seeking_alpha(self, symbol: str) -> pd.DataFrame:
        """Scrape news from Seeking Alpha"""
        try:
            url = f"https://seekingalpha.com/symbol/{symbol}/news"
            response = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            
            data = []
            for item in soup.select("h3 a, .sa-c-article-title a"):
                headline = item.get_text(strip=True)
                link = item.get("href", "")
                if headline and len(headline) > 10:
                    data.append({
                        "symbol": symbol,
                        "source": "Seeking Alpha",
                        "headline": headline,
                        "url": f"https://seekingalpha.com{link}" if link.startswith("/") else link,
                        "published_at": datetime.now().isoformat(),
                        "scraped_at": datetime.now().isoformat()
                    })
            
            logger.info(f"Seeking Alpha: Scraped {len(data)} articles for {symbol}")
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Seeking Alpha scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_cnbc(self, symbol: str) -> pd.DataFrame:
        """Scrape news from CNBC"""
        try:
            url = f"https://www.cnbc.com/quotes/{symbol}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            
            data = []
            for item in soup.select("a.QuotePageNewsStory-headline, h3 a"):
                headline = item.get_text(strip=True)
                link = item.get("href", "")
                if headline and len(headline) > 10:
                    data.append({
                        "symbol": symbol,
                        "source": "CNBC",
                        "headline": headline,
                        "url": f"https://www.cnbc.com{link}" if link.startswith("/") else link,
                        "published_at": datetime.now().isoformat(),
                        "scraped_at": datetime.now().isoformat()
                    })
            
            logger.info(f"CNBC: Scraped {len(data)} articles for {symbol}")
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"CNBC scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_benzinga(self, symbol: str) -> pd.DataFrame:
        """Scrape news from Benzinga"""
        try:
            url = f"https://www.benzinga.com/quote/{symbol}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            
            data = []
            for item in soup.select("h3 a, .article-title a"):
                headline = item.get_text(strip=True)
                link = item.get("href", "")
                if headline and len(headline) > 10:
                    data.append({
                        "symbol": symbol,
                        "source": "Benzinga",
                        "headline": headline,
                        "url": f"https://www.benzinga.com{link}" if link.startswith("/") else link,
                        "published_at": datetime.now().isoformat(),
                        "scraped_at": datetime.now().isoformat()
                    })
            
            logger.info(f"Benzinga: Scraped {len(data)} articles for {symbol}")
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Benzinga scraping failed for {symbol}: {e}")
            return pd.DataFrame()
    
    def scrape_all_sources(self, symbol: str, use_async: bool = True) -> pd.DataFrame:
        """Scrape from all available sources for a symbol with optional async support"""
        all_data = []
        
        sources = [
            self.scrape_yahoo_finance,
            self.scrape_reuters,
            self.scrape_marketwatch,
            self.scrape_finviz,
            self.scrape_seeking_alpha,
            self.scrape_cnbc,
            self.scrape_benzinga
        ]
        
        if use_async and len(sources) > 1:
            # Concurrent scraping for better performance
            with ThreadPoolExecutor(max_workers=min(len(sources), 5)) as executor:
                future_to_source = {executor.submit(source_func, symbol): source_func for source_func in sources}
                
                for future in as_completed(future_to_source):
                    source_func = future_to_source[future]
                    try:
                        df = future.result(timeout=20)
                        if not df.empty:
                            all_data.append(df)
                    except Exception as e:
                        logger.error(f"Error in {source_func.__name__}: {e}")
                        continue
        else:
            # Sequential scraping
            for source_func in sources:
                try:
                    df = source_func(symbol)
                    if not df.empty:
                        all_data.append(df)
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error in {source_func.__name__}: {e}")
                    continue
        
        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            combined.drop_duplicates(subset=["headline"], inplace=True)
            return combined
        return pd.DataFrame()
    
    def scrape_multiple_stocks(self, symbols: List[str] = None, use_async: bool = True) -> pd.DataFrame:
        """Scrape news for multiple stocks from all sources with optional async support"""
        symbols = symbols or self.symbols
        all_results = []
        
        if use_async and len(symbols) > 1:
            # Concurrent scraping for multiple stocks
            with ThreadPoolExecutor(max_workers=min(len(symbols), 3)) as executor:
                future_to_symbol = {executor.submit(self.scrape_all_sources, symbol, use_async=False): symbol 
                                   for symbol in symbols}
                
                for future in as_completed(future_to_symbol):
                    symbol = future_to_symbol[future]
                    try:
                        logger.info(f"Scraping news for {symbol}...")
                        df = future.result(timeout=60)
                        if not df.empty:
                            all_results.append(df)
                    except Exception as e:
                        logger.error(f"Error scraping {symbol}: {e}")
                        continue
        else:
            # Sequential scraping
            for symbol in symbols:
                logger.info(f"Scraping news for {symbol}...")
                df = self.scrape_all_sources(symbol, use_async=False)
                if not df.empty:
                    all_results.append(df)
                time.sleep(2)  # Rate limiting between stocks
        
        if all_results:
            final_df = pd.concat(all_results, ignore_index=True)
            final_df.drop_duplicates(subset=["headline", "symbol"], inplace=True)
            return final_df
        return pd.DataFrame()
    
    def save_results(self, df: pd.DataFrame, filename: str = "multisource_news.csv"):
        """Save scraped results to CSV"""
        if not df.empty:
            save_csv(df, f"data/raw/news/{filename}")
            logger.info(f"Saved {len(df)} articles to {filename}")
        else:
            logger.warning("No data to save")


if __name__ == "__main__":
    scraper = MultiSourceScraper(symbols=["AAPL", "MSFT", "TSLA", "GOOG"])
    results = scraper.scrape_multiple_stocks()
    scraper.save_results(results)

