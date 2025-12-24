import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://finance.yahoo.com/news"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_fallback():
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    for h in soup.select("h3"):
        text = h.get_text(strip=True)
        if text:
            headlines.append({"headline": text})

    return pd.DataFrame(headlines)
