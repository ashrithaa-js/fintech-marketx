import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.utils.helpers import save_csv
from src.scraping.scrap_news_fallback import scrape_fallback


URL = "https://www.reuters.com/markets/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def scrape_news():
    response = requests.get(URL, headers=HEADERS, timeout=15)

    print("HTTP STATUS:", response.status_code)

    if response.status_code != 200:
        print("Request blocked, using fallback...")
        df = scrape_fallback()
        save_csv(df, "data/raw/news/news_bs4.csv")
        return


    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []

    for tag in soup.select("a[role='heading']"):
        text = tag.get_text(strip=True)
        link = tag.get("href")

        if text:
            headlines.append({
                "headline": text,
                "url": f"https://www.reuters.com{link}"
            })

    df = pd.DataFrame(headlines)

    if df.empty:
        print("⚠ Reuters blocked. Switching to fallback source...")
        df = scrape_fallback()
        df['source'] = 'Fallback' 
        print(f"Scraped {len(df)} headlines from fallback source")
    else:
        df['source'] = 'Reuters'

    save_csv(df, "data/raw/news/news_bs4.csv")


if __name__ == "__main__":
    scrape_news()
