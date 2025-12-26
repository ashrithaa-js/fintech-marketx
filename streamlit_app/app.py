import path_setup  # noqa: F401
from src.utils.config import Config
import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Set minimal page config
st.set_page_config(
    page_title="Stock Intelligence Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# Stock Intelligence Platform\nEnhanced real-time stock market analytics"
    }
)


st.title("📈 Stock Market Intelligence Platform")
st.markdown("""
**Enhanced Real-time stock analytics using:**
- 🔄 **Multi-stock** live price data streaming
- 📰 **Multi-source** news sentiment (Yahoo, Reuters, MarketWatch, Finviz, Seeking Alpha, CNBC, Benzinga)
- 💰 **Comprehensive** financial statements scraping (Income, Balance Sheet, Cash Flow)
- 🤖 ML predictions with confidence scores
- 📊 **Dynamic** PowerBI integration with automated refresh
- 📈 Multi-stock comparison and analysis
""")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Multi-stock selector with custom input
st.sidebar.subheader("📊 Stock Selection")

# Allow custom stock input
custom_stock = st.sidebar.text_input(
    "Add Custom Stock Symbol",
    placeholder="e.g., NVDA, AMZN",
    help="Enter a stock symbol to add to the list"
)

# Update available stocks if custom stock is provided
available_stocks_list = list(Config.STOCKS)
if custom_stock and custom_stock.upper() not in available_stocks_list:
    available_stocks_list.append(custom_stock.upper())

# Multi-stock selector
available_stocks = st.sidebar.multiselect(
    "Select Stocks",
    options=available_stocks_list,
    default=[],
    help="Select one or more stocks to analyze"
)

# Auto-refresh option
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 Data Refresh")
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=False)
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 300, 30, disabled=not auto_refresh)

if auto_refresh:
    st.sidebar.info(f"Auto-refreshing every {refresh_interval} seconds")
    import time
    time.sleep(refresh_interval)
    st.rerun()

# Manual refresh button
if st.sidebar.button("🔄 Refresh Data Now", use_container_width=True):
    st.rerun()

# Quick stats
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Quick Stats")
st.sidebar.info(f"**Selected Stocks:** {len(available_stocks)}")

# Data status indicators
st.sidebar.markdown("---")
st.sidebar.subheader("📡 Data Status")

data_files = {
    "Price Data": "data/processed/features/features.csv",
    "News Data": "data/raw/news/multisource_news.csv",
    "Sentiment": "data/raw/sentiment/sentiment_scores.csv",
    "Predictions": "data/processed/features/predictions.csv",
    "Financials": "data/raw/fundamentals/income_statement.csv"
}

for name, path in data_files.items():
    if os.path.exists(path):
        st.sidebar.success(f"✓ {name}")
    else:
        st.sidebar.warning(f"⚠ {name}")

# Data Collection Buttons - Always Visible
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 To Start:")

# Collect Price Data Button
if st.sidebar.button("📊 Collect Price Data", use_container_width=True):
    with st.sidebar:
        with st.spinner("🔄 Collecting price data..."):
            try:
                from src.streaming.stream_prices import fetch_stock_price
                import pandas as pd
                from src.utils.helpers import save_csv
                
                symbols = available_stocks if available_stocks else Config.STOCKS
                all_prices = []
                
                # Ensure directories exist
                os.makedirs("data/raw/prices", exist_ok=True)
                os.makedirs("data/processed/features", exist_ok=True)
                
                for symbol in symbols:
                    df = fetch_stock_price(symbol, period="5d")
                    if not df.empty:
                        all_prices.append(df)
                
                if all_prices:
                    combined_df = pd.concat(all_prices, ignore_index=True)
                    save_csv(combined_df, "data/raw/prices/historical_prices.csv")
                    
                    latest_prices = combined_df.groupby('symbol').tail(1)
                    save_csv(latest_prices, "data/raw/prices/latest_price.csv")
                    
                    # Automatically generate features.csv from historical prices
                    st.sidebar.info("📊 Generating features...")
                    try:
                        # Create target column (next day price > current price)
                        features_df = combined_df.copy()
                        features_df["target"] = (features_df["Close"].shift(-1) > features_df["Close"]).astype(int)
                        features_df.dropna(inplace=True)
                        
                        # Select available columns for features
                        feature_cols = []
                        for col in ["Open", "High", "Low", "Close", "Volume", "target"]:
                            if col in features_df.columns:
                                feature_cols.append(col)
                        
                        if feature_cols:
                            features_output = features_df[feature_cols].copy()
                            features_output.to_csv("data/processed/features/features.csv", index=False)
                            st.sidebar.success(f"✅ Collected price data and generated features for {len(symbols)} stocks!")
                        else:
                            st.sidebar.warning("⚠️ Price data collected but couldn't generate features (missing columns)")
                    except Exception as feat_error:
                        st.sidebar.warning(f"⚠️ Price data collected but feature generation failed: {str(feat_error)[:100]}")
                    
                    st.rerun()
                else:
                    st.sidebar.error("❌ No price data collected")
            except Exception as e:
                st.sidebar.error(f"❌ Error: {e}")

# Scrape News Data Button
if st.sidebar.button("📰 Scrape News Data", use_container_width=True):
    with st.sidebar:
        with st.spinner("📰 Scraping news..."):
            try:
                os.makedirs("data/raw/news", exist_ok=True)
                os.makedirs("data/raw/sentiment", exist_ok=True)
                
                from src.scraping.multisource_scraper import MultiSourceScraper
                
                symbols = available_stocks if available_stocks else Config.STOCKS
                scraper = MultiSourceScraper(symbols=symbols)
                news_df = scraper.scrape_multiple_stocks(symbols=symbols, use_async=True)
                
                if news_df is not None and not news_df.empty:
                    scraper.save_results(news_df, "multisource_news.csv")
                    st.sidebar.success(f"✅ Scraped {len(news_df)} news articles!")
                    st.rerun()
                else:
                    st.sidebar.warning("⚠️ No news articles scraped")
            except Exception as e:
                st.sidebar.error(f"❌ Error: {e}")

# Scrape Financial Statements Button
if st.sidebar.button("💰 Scrape Financials", use_container_width=True):
    with st.sidebar:
        with st.spinner("💰 Scraping financials..."):
            try:
                os.makedirs("data/raw/fundamentals", exist_ok=True)
                
                from src.scraping.financial_statements_scraper import FinancialStatementsScraper
                
                symbols = available_stocks if available_stocks else Config.STOCKS
                scraper = FinancialStatementsScraper(symbols=symbols)
                statements = scraper.scrape_multiple_stocks(use_async=True)
                
                if statements:
                    scraper.save_statements(statements)
                    st.sidebar.success("✅ Scraped financial statements!")
                    st.rerun()
                else:
                    st.sidebar.warning("⚠️ No financial statements scraped")
            except Exception as e:
                st.sidebar.error(f"❌ Error: {e}")

# Generate ML Predictions Button
if st.sidebar.button("🤖 Generate Predictions", use_container_width=True):
    with st.sidebar:
        with st.spinner("🤖 Generating predictions..."):
            try:
                # Check if features file exists first
                features_file = "data/processed/features/features.csv"
                if not os.path.exists(features_file):
                    st.sidebar.error("❌ Features file not found!")
                    st.sidebar.info("💡 Please collect price data first to generate features.")
                    st.sidebar.info("Click '📊 Collect Price Data' button first.")
                    st.stop()
                
                # Check if model exists, train if not
                if not os.path.exists("model.pkl"):
                    st.sidebar.warning("⚠️ Model not found. Training model first...")
                    try:
                        from src.ml.train_model import train
                        train()
                        st.sidebar.success("✅ Model trained successfully!")
                    except Exception as train_error:
                        st.sidebar.error(f"❌ Model training failed: {str(train_error)[:200]}")
                        st.sidebar.info("💡 Make sure features.csv has valid data.")
                        st.stop()
                
                # Call predict function directly (better than subprocess)
                try:
                    from src.ml.predict import predict
                    predict()
                    
                    # Check if predictions file was created
                    if os.path.exists("data/processed/features/predictions.csv"):
                        st.sidebar.success("✅ Predictions generated successfully!")
                        st.rerun()
                    else:
                        st.sidebar.warning("⚠️ Predictions file not created. Check logs for errors.")
                except Exception as predict_error:
                    error_msg = str(predict_error)
                    st.sidebar.error(f"❌ Prediction error: {error_msg[:300]}")
                    if "sklearn" in error_msg.lower() or "scikit" in error_msg.lower():
                        st.sidebar.info("💡 Missing sklearn package. Install: pip install scikit-learn")
                    elif "model" in error_msg.lower():
                        st.sidebar.info("💡 Model issue. Try training the model again.")
                    
            except Exception as e:
                st.sidebar.error(f"❌ Error: {str(e)[:200]}")
                import traceback
                error_details = traceback.format_exc()[:400]
                with st.sidebar.expander("🔍 Error Details"):
                    st.code(error_details)

# PowerBI export button
st.sidebar.markdown("---")
if st.sidebar.button("📊 Export to PowerBI", use_container_width=True):
    try:
        from src.utils.powerbi_exporter import PowerBIExporter
        exporter = PowerBIExporter()
        exporter.export_all_data(symbols=available_stocks if available_stocks else [])
        st.sidebar.success("✓ Exported to PowerBI!")
    except Exception as e:
        st.sidebar.error(f"Export failed: {e}")

# Store selected stocks in session state
st.session_state['selected_stocks'] = available_stocks if available_stocks else []

# Main content area
st.sidebar.markdown("---")
st.sidebar.success("Select a page from above 👆")

# Display quick overview if on main page
if len(st.session_state.get('selected_stocks', [])) > 0:
    st.markdown("---")
    st.subheader("🚀 Quick Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_count = len(st.session_state.get('selected_stocks', []))
        st.metric("Selected Stocks", selected_count)
    
    with col2:
        # Count available data sources
        available_sources = sum(1 for path in data_files.values() if os.path.exists(path))
        st.metric("Data Sources", f"{available_sources}/{len(data_files)}")
    
    with col3:
        # Check if streaming is active
        if os.path.exists("data/raw/prices/latest_price.csv"):
            st.metric("Price Updates", "Active")
        else:
            st.metric("Price Updates", "Inactive")
    
    with col4:
        # Check PowerBI exports
        if os.path.exists("powerbi/data_sources/stock_prices.csv"):
            st.metric("PowerBI Data", "Ready")
        else:
            st.metric("PowerBI Data", "Not Exported")
