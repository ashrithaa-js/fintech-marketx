# src/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Paths
    DATA_PATH = "data/"
    RAW = "data/raw/"
    PROCESSED = "data/processed/"
    LOGS = "data/logs/"

    # Stocks
    STOCKS = ["AAPL", "TSLA", "MSFT", "GOOG", "NVDA"]

    # API / URLs
    API_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")
    NEWS_URL = "https://www.reuters.com/markets/"
