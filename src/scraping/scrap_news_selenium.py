from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from src.utils.helpers import save_csv
import time
from src.scraping.scrap_news_fallback import scrape_fallback


def scrape_news_selenium():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.reuters.com/markets/")
    wait = WebDriverWait(driver, 30)

    # Let JS settle
    time.sleep(10)

    headlines = []

    elements = driver.find_elements(By.XPATH, "//a[@role='heading']")

    for el in elements:
        text = el.text.strip()
        link = el.get_attribute("href")
        if len(text) > 15:
            headlines.append({
                "headline": text,
                "url": link
            })

    df = pd.DataFrame(headlines)

    if df.empty:
        print("⚠ Selenium blocked. Switching to fallback source...")
        df = scrape_fallback()
        df['source'] = 'Fallback'  
        print(f"Scraped {len(df)} headlines from fallback source") 

    else:
        print(f"Scraped {len(df)} headlines")
        df['source'] = 'Reuters' 

    save_csv(df, "data/raw/news/news_selenium.csv")
    driver.quit()

if __name__ == "__main__":
    scrape_news_selenium()
