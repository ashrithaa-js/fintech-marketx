"""
Master script to run all improved features of the Stock Intelligence Platform
"""
import os
import sys
from datetime import datetime
from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Run all data collection and processing steps"""
    print("=" * 60)
    print("🚀 Stock Intelligence Platform - Enhanced Features")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    symbols = Config.STOCKS
    print(f"📊 Processing stocks: {', '.join(symbols)}\n")
    
    # Step 1: Multi-source news scraping
    print("=" * 60)
    print("Step 1: Multi-source News Scraping")
    print("=" * 60)
    try:
        from src.scraping.multisource_scraper import MultiSourceScraper
        scraper = MultiSourceScraper(symbols=symbols)
        news_df = scraper.scrape_multiple_stocks(symbols=symbols, use_async=True)
        scraper.save_results(news_df, "multisource_news.csv")
        print(f"✓ Scraped {len(news_df)} news articles from multiple sources\n")
    except Exception as e:
        logger.error(f"News scraping failed: {e}")
        print(f"✗ News scraping failed: {e}\n")
    
    # Step 2: Financial statements scraping
    print("=" * 60)
    print("Step 2: Financial Statements Scraping")
    print("=" * 60)
    try:
        from src.scraping.financial_statements_scraper import FinancialStatementsScraper
        fin_scraper = FinancialStatementsScraper(symbols=symbols)
        statements = fin_scraper.scrape_multiple_stocks(symbols=symbols, use_async=True)
        fin_scraper.save_statements(statements)
        total_records = sum(len(df) for df in statements.values() if not df.empty)
        print(f"✓ Scraped {total_records} financial statement records\n")
    except Exception as e:
        logger.error(f"Financial statements scraping failed: {e}")
        print(f"✗ Financial statements scraping failed: {e}\n")
    
    # Step 3: PowerBI export
    print("=" * 60)
    print("Step 3: PowerBI Data Export")
    print("=" * 60)
    try:
        from src.utils.powerbi_exporter import PowerBIExporter
        exporter = PowerBIExporter()
        exporter.export_all_data(symbols=symbols)
        exporter.create_data_model_summary(symbols=symbols)
        print("✓ PowerBI data exported successfully\n")
    except Exception as e:
        logger.error(f"PowerBI export failed: {e}")
        print(f"✗ PowerBI export failed: {e}\n")
    
    print("=" * 60)
    print("✅ All improvements completed!")
    print("=" * 60)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("Next steps:")
    print("1. Start price streaming: python src/streaming/stream_prices.py")
    print("2. Run sentiment analysis on news data")
    print("3. Train/update ML model: python src/ml/train_model.py")
    print("4. Generate predictions: python src/ml/predict.py")
    print("5. Launch Streamlit app: streamlit run streamlit_app/app.py")

if __name__ == "__main__":
    main()

