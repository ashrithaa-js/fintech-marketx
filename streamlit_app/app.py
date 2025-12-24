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
