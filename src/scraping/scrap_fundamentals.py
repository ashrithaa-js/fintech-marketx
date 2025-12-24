import yfinance as yf
import pandas as pd
from src.utils.helpers import save_csv

def scrape_fundamentals(ticker="AAPL"):
    stock = yf.Ticker(ticker)
    data = stock.financials
    save_csv(data.reset_index(), "data/raw/fundamentals/fundamentals.csv")

if __name__ == "__main__":
    scrape_fundamentals()
