# Stock Intelligence Platform

A comprehensive real-time stock market data engineering + ML prediction system with enhanced multi-source data collection, dynamic PowerBI integration, and advanced Streamlit dashboard.

## 🚀 Enhanced Features

### ✨ Recent Improvements

1. **🔍 Enhanced Multi-Source Scraping**
   - Concurrent/async scraping for improved performance
   - Support for 7+ news sources: Yahoo Finance, Reuters, MarketWatch, Finviz, Seeking Alpha, CNBC, Benzinga
   - Better error handling and rate limiting
   - Automatic deduplication of articles

2. **📊 Dynamic PowerBI Integration**
   - Automated data export with scheduled refresh capability
   - Comprehensive data model with relationships
   - Timestamped backups for version control
   - PowerShell script for Windows Task Scheduler integration
   - Support for multiple stocks simultaneously

3. **💰 Enhanced Financial Statements Scraper**
   - Quarterly and annual data collection
   - Historical data support
   - Concurrent scraping for multiple stocks
   - Comprehensive Income Statement, Balance Sheet, and Cash Flow data

4. **📈 Multi-Stock Support**
   - Simultaneous price streaming for multiple stocks
   - Enhanced comparison features across all components
   - Individual and combined data exports

5. **🎨 Improved Streamlit Dashboard**
   - Real-time auto-refresh capability
   - Enhanced multi-stock comparison visualizations
   - Better UI/UX with data status indicators
   - Custom stock symbol input
   - One-click PowerBI export
   - Comprehensive ML predictions page with accuracy metrics

## 📋 System Components

- **Live Stream Data**: Real-time price streaming for multiple stocks
- **Multi-Source Scraping**: News from 7+ sources with async support
- **Spark Streaming**: Real-time data processing
- **NLP Sentiment Analysis**: News sentiment scoring
- **ML Predictions**: Stock price predictions with confidence scores
- **Power BI Dashboarding**: Dynamic data export and visualization
- **Streamlit Web App**: Interactive dashboard with real-time updates

## 🏗️ Project Structure

```
stock-intelligence-platform/
├── data/
│   ├── raw/              # Raw scraped data
│   │   ├── news/         # Multi-source news articles
│   │   ├── prices/       # Stock price data
│   │   ├── fundamentals/ # Financial statements
│   │   └── sentiment/    # Sentiment scores
│   ├── processed/        # Processed features and predictions
│   └── logs/             # System logs
├── src/
│   ├── scraping/         # Web scrapers
│   │   ├── multisource_scraper.py      # Enhanced multi-source news scraper
│   │   └── financial_statements_scraper.py  # Financial data scraper
│   ├── streaming/        # Real-time data streaming
│   │   └── stream_prices.py            # Multi-stock price streaming
│   ├── sentiment/        # Sentiment analysis
│   ├── ml/               # Machine learning models
│   └── utils/             # Utilities
│       ├── powerbi_exporter.py        # Dynamic PowerBI exporter
│       ├── config.py      # Configuration
│       └── logger.py      # Logging utilities
├── streamlit_app/        # Streamlit web application
│   ├── app.py           # Main app
│   └── pages/           # Dashboard pages
│       ├── 1_Market_Overview.py
│       ├── 2_Sentiment_Analysis.py
│       ├── 3_Fundamentals.py
│       └── 4_ML_Predictions.py
├── powerbi/             # PowerBI dashboards and data
│   └── data_sources/    # Exported data for PowerBI
└── notebooks/           # Jupyter notebooks for analysis
```

## 🚀 Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Or use setup script
bash setup.sh
```

### 2. Run All Improvements

```bash
# Run comprehensive data collection
python run_all_improvements.py
```

This will:
- Scrape news from multiple sources for all configured stocks
- Collect financial statements
- Export data to PowerBI format

### 3. Start Price Streaming

```bash
# Stream prices for multiple stocks
python src/streaming/stream_prices.py
```

### 4. Launch Streamlit Dashboard

```bash
streamlit run streamlit_app/app.py
```

## 📊 Usage Guide

### Multi-Source News Scraping

```python
from src.scraping.multisource_scraper import MultiSourceScraper

scraper = MultiSourceScraper(symbols=["AAPL", "MSFT", "TSLA"])
# Async scraping for better performance
news_df = scraper.scrape_multiple_stocks(use_async=True)
scraper.save_results(news_df)
```

### Financial Statements Scraping

```python
from src.scraping.financial_statements_scraper import FinancialStatementsScraper

fin_scraper = FinancialStatementsScraper(symbols=["AAPL", "MSFT"])
statements = fin_scraper.scrape_multiple_stocks(use_async=True)
fin_scraper.save_statements(statements)
```

### PowerBI Export

```python
from src.utils.powerbi_exporter import PowerBIExporter

exporter = PowerBIExporter()
exporter.export_all_data(symbols=["AAPL", "MSFT", "TSLA"])
exporter.create_data_model_summary()
exporter.create_refresh_script(refresh_interval_minutes=15)
```

### Multi-Stock Price Streaming

```python
from src.streaming.stream_prices import stream_prices
from src.utils.config import Config

# Stream prices for all configured stocks
stream_prices(symbols=Config.STOCKS, interval=60)
```

## 🔧 Configuration

Edit `src/utils/config.py` to customize:

```python
class Config:
    STOCKS = ["AAPL", "MSFT", "TSLA", "GOOG"]  # Add your stocks here
    DATA_PATH = "data/"
    # ... other settings
```

## 📈 PowerBI Integration

### Automated Refresh Setup

1. Run the PowerBI exporter to generate refresh script:
   ```bash
   python src/utils/powerbi_exporter.py
   ```

2. Set up Windows Task Scheduler:
   - Action: `powershell.exe`
   - Arguments: `-File powerbi/data_sources/refresh_data.ps1`
   - Trigger: Every 15 minutes (or as needed)

### Data Model

The PowerBI exporter creates:
- `stock_prices.csv` - Historical price data
- `news_data.csv` - Multi-source news articles
- `sentiment_data.csv` - Sentiment scores
- `income_statement_powerbi.csv` - Income statements
- `balance_sheet_powerbi.csv` - Balance sheets
- `cash_flow_powerbi.csv` - Cash flow statements
- `ml_predictions.csv` - ML predictions
- `data_model_summary.json` - Data model documentation

## 🎨 Streamlit Dashboard Features

### Pages

1. **Market Overview**: Multi-stock price comparison, volume analysis, summary statistics
2. **Sentiment Analysis**: News sentiment distribution, source analysis, latest articles
3. **Fundamentals**: Financial statements visualization and comparison
4. **ML Predictions**: Prediction trends, accuracy metrics, confidence scores

### Features

- ✅ Multi-stock selection and comparison
- ✅ Real-time auto-refresh (configurable interval)
- ✅ Custom stock symbol input
- ✅ Data status indicators
- ✅ One-click PowerBI export
- ✅ Interactive visualizations with Plotly
- ✅ Download data as CSV

## 📦 Dependencies

See `requirements.txt` for full list. Key dependencies:
- pandas, numpy
- yfinance
- requests, beautifulsoup4, selenium
- streamlit, plotly
- scikit-learn, nltk
- pyspark

## 🔄 Data Flow

```
1. Multi-Source Scraping → News Articles
2. Price Streaming → Historical Prices
3. Financial Scraping → Financial Statements
4. Sentiment Analysis → Sentiment Scores
5. Feature Engineering → ML Features
6. ML Training → Prediction Model
7. Predictions → Forecast Results
8. PowerBI Export → Dashboard Data
```

## 📝 Notes

- The system supports concurrent/async operations for better performance
- All scrapers include rate limiting to respect website policies
- Data is automatically deduplicated and validated
- Logs are stored in `data/logs/system.log`
- PowerBI exports include timestamped backups

## 🤝 Contributing

Feel free to extend the platform with:
- Additional news sources
- More financial data sources (SEC EDGAR, etc.)
- Enhanced ML models
- Additional visualizations

## 📄 License

This project is for educational and research purposes.
