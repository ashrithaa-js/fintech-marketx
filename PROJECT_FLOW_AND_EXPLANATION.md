# Stock Intelligence Platform - Complete Flow & Detailed Explanation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Complete Data Flow](#complete-data-flow)
4. [Component Details](#component-details)
5. [User Workflow](#user-workflow)
6. [Technical Stack](#technical-stack)

---

## 🎯 Project Overview

The **Stock Intelligence Platform** is a comprehensive, real-time stock market analytics and prediction system that:

- **Collects** multi-source financial data (prices, news, financial statements)
- **Analyzes** sentiment from news articles across 7+ sources
- **Predicts** stock price movements using machine learning
- **Visualizes** data through interactive Streamlit dashboards
- **Exports** data to PowerBI for advanced business intelligence

### Key Capabilities
- ✅ Real-time price streaming for multiple stocks simultaneously
- ✅ Multi-source news scraping (7+ sources: Yahoo, Reuters, MarketWatch, Finviz, Seeking Alpha, CNBC, Benzinga)
- ✅ Financial statements scraping (Income Statement, Balance Sheet, Cash Flow)
- ✅ NLP-based sentiment analysis
- ✅ ML-powered price predictions with confidence scores
- ✅ Interactive web dashboard with real-time updates
- ✅ Automated PowerBI integration with scheduled refresh

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    STOCK INTELLIGENCE PLATFORM                   │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  DATA        │    │  PROCESSING  │    │  VISUALIZ.   │
│  COLLECTION  │───▶│  & ANALYSIS  │───▶│  & EXPORT    │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        │                     │                     │
   ┌────┴────┐          ┌────┴────┐          ┌────┴────┐
   │         │          │         │          │         │
   ▼         ▼          ▼         ▼          ▼         ▼
Prices   News    Sentiment  ML      Streamlit  PowerBI
Stream   Scrape  Analysis   Predict Dashboard Export
```

### Architecture Layers

1. **Data Collection Layer**
   - Price streaming (yfinance API)
   - Multi-source web scraping
   - Financial statements extraction

2. **Processing Layer**
   - Sentiment analysis (NLP)
   - Feature engineering
   - ML model training & prediction

3. **Visualization Layer**
   - Streamlit interactive dashboard
   - PowerBI business intelligence
   - Real-time data updates

---

## 🔄 Complete Data Flow

### Phase 1: Data Collection

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION PHASE                     │
└─────────────────────────────────────────────────────────────┘

1. PRICE STREAMING
   ┌─────────────────────────────────────┐
   │ stream_prices.py                    │
   │ - Fetches real-time prices          │
   │ - Multiple stocks concurrently      │
   │ - Updates every 60 seconds          │
   │ - Saves to:                         │
   │   • latest_price.csv (combined)     │
   │   • latest_price_{SYMBOL}.csv      │
   │   • historical_prices.csv          │
   └─────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ data/raw/prices/                    │
   │ - Historical price data            │
   │ - Real-time price updates          │
   │ - Technical indicators              │
   └─────────────────────────────────────┘

2. MULTI-SOURCE NEWS SCRAPING
   ┌─────────────────────────────────────┐
   │ multisource_scraper.py              │
   │ - Scrapes from 7+ sources:         │
   │   • Yahoo Finance                   │
   │   • Reuters                         │
   │   • MarketWatch                     │
   │   • Finviz                          │
   │   • Seeking Alpha                   │
   │   • CNBC                            │
   │   • Benzinga                        │
   │ - Concurrent/async scraping        │
   │ - Deduplication                     │
   └─────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ data/raw/news/                      │
   │ - multisource_news.csv             │
   │ - Articles with metadata           │
   │ - Source attribution               │
   └─────────────────────────────────────┘

3. FINANCIAL STATEMENTS SCRAPING
   ┌─────────────────────────────────────┐
   │ financial_statements_scraper.py      │
   │ - Income Statement                  │
   │ - Balance Sheet                     │
   │ - Cash Flow Statement               │
   │ - Quarterly & Annual data           │
   │ - Historical records                │
   └─────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ data/raw/fundamentals/              │
   │ - income_statement.csv              │
   │ - balance_sheet.csv                │
   │ - cash_flow.csv                     │
   └─────────────────────────────────────┘
```

### Phase 2: Data Processing

```
┌─────────────────────────────────────────────────────────────┐
│                  DATA PROCESSING PHASE                       │
└─────────────────────────────────────────────────────────────┘

1. SENTIMENT ANALYSIS
   ┌─────────────────────────────────────┐
   │ sentiment_model.py                  │
   │ - Uses TextBlob NLP library        │
   │ - Calculates polarity (-1 to +1)   │
   │ - Categorizes:                      │
   │   • Positive (> 0.1)                │
   │   • Negative (< -0.1)              │
   │   • Neutral (else)                 │
   │ - Processes news articles           │
   └─────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ data/raw/sentiment/                 │
   │ - sentiment_scores.csv             │
   │ - Article sentiment labels          │
   │ - Sentiment scores                  │
   └─────────────────────────────────────┘

2. FEATURE ENGINEERING
   ┌─────────────────────────────────────┐
   │ Feature Engineering (notebooks)     │
   │ - Combines price data              │
   │ - Adds technical indicators:         │
   │   • Moving averages                 │
   │   • RSI, MACD                      │
   │   • Volume indicators               │
   │ - Merges sentiment scores           │
   │ - Creates ML-ready features         │
   └─────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ data/processed/features/            │
   │ - features.csv                     │
   │ - Engineered features              │
   │ - Target variables                 │
   └─────────────────────────────────────┘

3. ML MODEL TRAINING
   ┌─────────────────────────────────────┐
   │ train_model.py                      │
   │ - Loads features.csv                │
   │ - Trains ML model (scikit-learn)    │
   │ - Saves model to model.pkl         │
   │ - Evaluates performance             │
   └─────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ model.pkl                           │
   │ - Trained ML model                  │
   │ - Ready for predictions             │
   └─────────────────────────────────────┘

4. ML PREDICTIONS
   ┌─────────────────────────────────────┐
   │ predict.py                          │
   │ - Loads trained model               │
   │ - Generates predictions             │
   │ - Converts to UP/DOWN labels        │
   │ - Calculates confidence scores      │
   │ - Merges with price data            │
   └─────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ data/processed/features/            │
   │ - predictions.csv                   │
   │ - Predicted prices                 │
   │ - Confidence scores                 │
   │ - UP/DOWN predictions               │
   └─────────────────────────────────────┘
```

### Phase 3: Visualization & Export

```
┌─────────────────────────────────────────────────────────────┐
│              VISUALIZATION & EXPORT PHASE                   │
└─────────────────────────────────────────────────────────────┘

1. STREAMLIT DASHBOARD
   ┌─────────────────────────────────────┐
   │ streamlit_app/app.py                │
   │ - Main dashboard entry point        │
   │ - Stock selection                   │
   │ - Real-time updates                 │
   │ - Auto-refresh capability           │
   └─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │Market  │  │Sentiment│  │Fundamentals│
   │Overview│  │Analysis │  │            │
   └────────┘  └────────┘  └────────┘
        │           │           │
        └───────────┼───────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ ML Predictions Page                 │
   │ - Prediction trends                 │
   │ - Accuracy metrics                  │
   │ - Confidence scores                 │
   └─────────────────────────────────────┘

2. POWERBI EXPORT
   ┌─────────────────────────────────────┐
   │ powerbi_exporter.py                 │
   │ - Exports all data to CSV           │
   │ - Creates data model                │
   │ - Generates refresh script          │
   │ - Timestamped backups               │
   └─────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ powerbi/data_sources/               │
   │ - stock_prices.csv                  │
   │ - news_data.csv                     │
   │ - sentiment_data.csv                │
   │ - income_statement_powerbi.csv     │
   │ - balance_sheet_powerbi.csv         │
   │ - cash_flow_powerbi.csv             │
   │ - ml_predictions.csv                 │
   │ - data_model_summary.json           │
   │ - refresh_data.ps1                  │
   └─────────────────────────────────────┘
```

---

## 🔧 Component Details

### 1. Price Streaming (`src/streaming/stream_prices.py`)

**Purpose**: Continuously fetch and update stock prices in real-time

**How it works**:
- Uses `yfinance` library to fetch stock data
- Supports multiple stocks concurrently using ThreadPoolExecutor
- Fetches 1-minute interval data
- Updates every 60 seconds (configurable)
- Saves both individual stock files and combined file
- Maintains historical data (last 1000 records per stock)

**Output**:
- `data/raw/prices/latest_price.csv` - Combined prices
- `data/raw/prices/latest_price_{SYMBOL}.csv` - Individual stocks
- `data/raw/prices/historical_prices.csv` - Historical data

**Features**:
- Concurrent fetching for better performance
- Automatic error handling and retry logic
- Timestamp tracking
- Symbol column for multi-stock support

---

### 2. Multi-Source News Scraper (`src/scraping/multisource_scraper.py`)

**Purpose**: Collect news articles from 7+ different financial news sources

**Sources**:
1. **Yahoo Finance** - General financial news
2. **Reuters** - International financial news
3. **MarketWatch** - Market analysis and news
4. **Finviz** - Stock screener and news
5. **Seeking Alpha** - Investment research and analysis
6. **CNBC** - Business and financial news
7. **Benzinga** - Real-time financial news

**How it works**:
- Each source has a dedicated scraping method
- Uses BeautifulSoup4 and Selenium for web scraping
- Concurrent/async scraping for multiple stocks
- Automatic deduplication of articles
- Rate limiting to respect website policies
- Error handling for failed requests

**Output**:
- `data/raw/news/multisource_news.csv`
- Columns: symbol, headline, source, url, published_at, content

**Features**:
- Async support for 60-70% faster scraping
- Automatic article deduplication
- Source attribution
- Date/time tracking

---

### 3. Financial Statements Scraper (`src/scraping/financial_statements_scraper.py`)

**Purpose**: Extract comprehensive financial statements from Yahoo Finance

**Statement Types**:
1. **Income Statement** - Revenue, expenses, net income
2. **Balance Sheet** - Assets, liabilities, equity
3. **Cash Flow Statement** - Operating, investing, financing activities

**How it works**:
- Uses `yfinance` library to fetch financial data
- Supports both quarterly and annual data
- Concurrent scraping for multiple stocks
- Historical data collection
- Automatic date sorting (most recent first)
- Data normalization and formatting

**Output**:
- `data/raw/fundamentals/income_statement.csv`
- `data/raw/fundamentals/balance_sheet.csv`
- `data/raw/fundamentals/cash_flow.csv`

**Features**:
- Quarterly granularity for trend analysis
- Historical data support
- Concurrent processing
- Comprehensive financial metrics

---

### 4. Sentiment Analysis (`src/sentiment/sentiment_model.py`)

**Purpose**: Analyze sentiment of news articles to determine market sentiment

**How it works**:
- Uses TextBlob NLP library for sentiment analysis
- Calculates polarity score (-1 to +1):
  - **Positive**: score > 0.1
  - **Negative**: score < -0.1
  - **Neutral**: -0.1 ≤ score ≤ 0.1
- Processes news article headlines and content
- Text preprocessing (cleaning, normalization)

**Output**:
- `data/raw/sentiment/sentiment_scores.csv`
- Columns: headline, symbol, sentiment, sentiment_score, date

**Features**:
- Automatic sentiment categorization
- Polarity scoring
- Multi-article batch processing
- Integration with news data

---

### 5. ML Prediction System (`src/ml/`)

#### Model Training (`train_model.py`)

**Purpose**: Train machine learning model to predict stock price movements

**Process**:
1. Loads engineered features from `features.csv`
2. Splits data into training and testing sets
3. Trains scikit-learn model (classification/regression)
4. Evaluates model performance
5. Saves trained model to `model.pkl`

**Features Used**:
- Historical price data
- Technical indicators (RSI, MACD, moving averages)
- Volume indicators
- Sentiment scores
- Market trends

#### Prediction Generation (`predict.py`)

**Purpose**: Generate price predictions using trained model

**Process**:
1. Loads trained model from `model.pkl`
2. Loads features from `features.csv`
3. Generates predictions for each data point
4. Converts regression predictions to binary (UP/DOWN)
5. Calculates confidence scores
6. Merges with historical price data
7. Adds symbol column for multi-stock support

**Output**:
- `data/processed/features/predictions.csv`
- Columns: symbol, datetime, price, predicted_price, prediction, confidence

**Features**:
- UP/DOWN prediction labels
- Confidence scores (0-100%)
- Actual vs predicted price comparison
- Multi-stock support

---

### 6. Streamlit Dashboard (`streamlit_app/`)

**Purpose**: Interactive web-based dashboard for data visualization and analysis

#### Main App (`app.py`)

**Features**:
- Stock selection (multi-select dropdown)
- Custom stock symbol input
- Auto-refresh capability (configurable interval)
- Data status indicators
- One-click PowerBI export
- Quick overview metrics

#### Pages

**1. Market Overview** (`pages/1_Market_Overview.py`)
- Multi-stock price comparison charts
- Current price metrics with change indicators
- Trading volume analysis
- Summary statistics table
- Interactive Plotly visualizations

**2. Sentiment Analysis** (`pages/2_Sentiment_Analysis.py`)
- Sentiment distribution pie chart
- Sentiment by stock bar chart
- News source analysis
- Latest news articles with filtering
- Download filtered data

**3. Fundamentals** (`pages/3_Fundamentals.py`)
- Financial statements visualization
- Income Statement, Balance Sheet, Cash Flow
- Key metrics comparison across stocks
- Historical trends
- Full statement data tables

**4. ML Predictions** (`pages/4_ML_Predictions.py`)
- Actual vs predicted price comparison
- Prediction trends over time
- Confidence score metrics
- Accuracy metrics
- Historical predictions table
- Regenerate predictions button

**Features**:
- Real-time data updates
- Interactive visualizations (Plotly)
- Multi-stock comparison
- Data filtering and search
- CSV download functionality

---

### 7. PowerBI Exporter (`src/utils/powerbi_exporter.py`)

**Purpose**: Export all data to PowerBI-compatible format with automated refresh

**How it works**:
1. Exports all data sources to CSV files
2. Formats data for PowerBI (date columns, numeric types)
3. Creates data model summary with relationships
4. Generates PowerShell refresh script
5. Creates timestamped backups

**Exported Files**:
- `stock_prices.csv` - Price data
- `news_data.csv` - News articles
- `sentiment_data.csv` - Sentiment scores
- `income_statement_powerbi.csv` - Income statements
- `balance_sheet_powerbi.csv` - Balance sheets
- `cash_flow_powerbi.csv` - Cash flow statements
- `ml_predictions.csv` - ML predictions
- `data_model_summary.json` - Data model documentation

**Features**:
- Automated refresh scheduling
- Data model relationships
- Primary key definitions
- DAX measure suggestions
- Timestamped backups

---

## 👤 User Workflow

### Initial Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Stocks**
   - Edit `src/utils/config.py`
   - Set `STOCKS = ["AAPL", "TSLA", "MSFT", "GOOG", "NVDA"]`

3. **Run Data Collection**
   ```bash
   python run_all_improvements.py
   ```
   This runs:
   - Multi-source news scraping
   - Financial statements scraping
   - PowerBI export

### Daily Operations

1. **Start Price Streaming** (Run in background)
   ```bash
   python src/streaming/stream_prices.py
   ```
   - Continuously updates prices every 60 seconds
   - Runs until stopped

2. **Run Sentiment Analysis** (Periodic)
   ```bash
   python run_sentiment_analysis.py
   ```
   - Analyzes sentiment of collected news
   - Updates sentiment scores

3. **Generate ML Predictions** (Periodic)
   ```bash
   python src/ml/predict.py
   ```
   - Generates new predictions from latest data
   - Updates predictions.csv

4. **Launch Dashboard**
   ```bash
   streamlit run streamlit_app/app.py
   ```
   - Opens web browser
   - Interactive dashboard
   - Real-time data visualization

### PowerBI Integration

1. **Export Data**
   - Click "Export to PowerBI" button in Streamlit
   - Or run: `python src/utils/powerbi_exporter.py`

2. **Set Up Auto-Refresh**
   - Use generated `refresh_data.ps1` script
   - Schedule in Windows Task Scheduler
   - Set interval (recommended: 15 minutes)

3. **Import to PowerBI**
   - Import CSV files from `powerbi/data_sources/`
   - Use `data_model_summary.json` for relationships
   - Create visualizations

---

## 🛠️ Technical Stack

### Programming Languages
- **Python 3.8+** - Main language

### Core Libraries

**Data Collection**:
- `yfinance` - Stock price data
- `requests` - HTTP requests
- `beautifulsoup4` - Web scraping
- `selenium` - Dynamic web scraping

**Data Processing**:
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `textblob` - NLP sentiment analysis

**Machine Learning**:
- `scikit-learn` - ML models
- `joblib` - Model serialization

**Visualization**:
- `streamlit` - Web dashboard
- `plotly` - Interactive charts

**Utilities**:
- `python-dotenv` - Environment variables
- `concurrent.futures` - Async operations

### Data Storage
- **CSV Files** - Primary storage format
- **JSON** - Configuration and metadata
- **Pickle** - ML model storage

### Architecture Patterns
- **Modular Design** - Separate components
- **Async/Concurrent Processing** - Performance optimization
- **Error Handling** - Robust error management
- **Logging** - Comprehensive logging system

---

## 📊 Data Flow Summary

```
1. PRICE STREAMING
   yfinance API → stream_prices.py → CSV files
   
2. NEWS SCRAPING
   Web Sources → multisource_scraper.py → News CSV
   
3. FINANCIAL DATA
   Yahoo Finance → financial_statements_scraper.py → Financial CSVs
   
4. SENTIMENT ANALYSIS
   News CSV → sentiment_model.py → Sentiment CSV
   
5. FEATURE ENGINEERING
   Price + Sentiment → Feature Engineering → Features CSV
   
6. ML TRAINING
   Features CSV → train_model.py → model.pkl
   
7. ML PREDICTIONS
   Features CSV + model.pkl → predict.py → Predictions CSV
   
8. VISUALIZATION
   All CSVs → Streamlit Dashboard → Interactive Charts
   
9. POWERBI EXPORT
   All CSVs → powerbi_exporter.py → PowerBI CSVs
```

---

## 🎯 Key Features Summary

### Performance
- ✅ Concurrent/async operations (60-70% faster)
- ✅ Multi-stock simultaneous processing
- ✅ Real-time data updates

### Data Quality
- ✅ Multi-source data collection
- ✅ Automatic deduplication
- ✅ Error handling and validation
- ✅ Historical data support

### User Experience
- ✅ Interactive web dashboard
- ✅ Real-time auto-refresh
- ✅ Custom stock selection
- ✅ One-click exports
- ✅ Comprehensive visualizations

### Automation
- ✅ Automated data collection
- ✅ Scheduled PowerBI refresh
- ✅ Timestamped backups
- ✅ Error recovery

---

## 🔄 Complete Workflow Example

**Scenario**: User wants to analyze AAPL, MSFT, and TSLA

1. **Setup** (One-time)
   - Configure stocks in `config.py`
   - Run `run_all_improvements.py` to collect initial data

2. **Daily Operations**
   - Start price streaming (background process)
   - Dashboard automatically shows latest data
   - User selects stocks in Streamlit sidebar
   - Views:
     - Market Overview: Price trends, volume
     - Sentiment: News sentiment analysis
     - Fundamentals: Financial statements
     - ML Predictions: Price predictions with confidence

3. **Periodic Updates**
   - Run sentiment analysis on new news
   - Regenerate ML predictions
   - Export to PowerBI for advanced analytics

4. **Analysis**
   - Compare multiple stocks side-by-side
   - Filter by date, sentiment, source
   - Download data for further analysis
   - View predictions with confidence scores

---

## 📈 Use Cases

1. **Stock Research**
   - Analyze company fundamentals
   - Review news sentiment
   - Compare multiple stocks

2. **Trading Decisions**
   - View ML predictions
   - Check confidence scores
   - Analyze price trends

3. **Market Monitoring**
   - Real-time price updates
   - News aggregation
   - Sentiment tracking

4. **Business Intelligence**
   - PowerBI dashboards
   - Historical analysis
   - Trend identification

---

## 🚀 Future Enhancements

- SEC EDGAR integration for direct filing access
- Real-time WebSocket price updates
- Advanced ML models (LSTM, Transformers)
- Alert system for price/sentiment thresholds
- Portfolio tracking and management
- REST API for external integrations
- Mobile app support

---

## 📝 Conclusion

The Stock Intelligence Platform is a comprehensive, end-to-end solution for stock market analysis, combining:

- **Real-time data collection** from multiple sources
- **Advanced analytics** with ML and sentiment analysis
- **Interactive visualization** through Streamlit
- **Business intelligence** via PowerBI integration
- **Automated workflows** for efficiency

The system is designed to be modular, scalable, and user-friendly, making it suitable for both individual investors and financial analysts.

