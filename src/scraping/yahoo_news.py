import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_yahoo(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/news"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    data = []
    for item in soup.select("h3"):
        data.append({
            "symbol": symbol,
            "source": "Yahoo Finance",
            "headline": item.text,
            "published_at": datetime.now()
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = scrape_yahoo("AAPL")
    df.to_csv("data/raw/news/yahoo_AAPL.csv", index=False)
