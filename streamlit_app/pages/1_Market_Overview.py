import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Ensure project root on sys.path for src.* imports
from streamlit_app import path_setup  # noqa: F401
from src.utils.config import Config

st.header("📊 Market Overview")

# Get selected stocks from session state
selected_stocks = st.session_state.get('selected_stocks', [])

# Load data with error handling
try:
    # Try historical_prices.csv first (has symbol column), then fallback to features.csv
    price_files = [
        "data/raw/prices/historical_prices.csv",
        "data/processed/features/features.csv"
    ]
    
    df = None
    price_file = None
    
    for file_path in price_files:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                price_file = file_path
                break
            except Exception as e:
                continue
    
    if df is not None and not df.empty:
        # Handle different column names
        # historical_prices.csv uses: Datetime, Close, symbol
        # features.csv uses: Open, High, Low, Close, Volume (no symbol)
        
        # Map column names
        datetime_col = None
        price_col = None
        
        if "Datetime" in df.columns:
            datetime_col = "Datetime"
        elif "datetime" in df.columns:
            datetime_col = "datetime"
        elif "Date" in df.columns:
            datetime_col = "Date"
        
        if "Close" in df.columns:
            price_col = "Close"
        elif "price" in df.columns:
            price_col = "price"
        
        # Filter by selected stocks if symbol column exists
        if "symbol" in df.columns:
            stocks_to_filter = selected_stocks if selected_stocks else Config.STOCKS
            df = df[df["symbol"].isin(stocks_to_filter)]
            
            # Convert datetime if needed
            if datetime_col:
                df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
                df = df.sort_values(datetime_col)
            
            # Multi-stock price comparison
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if datetime_col and price_col:
                    fig = px.line(
                        df,
                        x=datetime_col,
                        y=price_col,
                        color="symbol",
                        title="Multi-Stock Price Comparison",
                        labels={price_col: "Price ($)", datetime_col: "Date"},
                        markers=True
                    )
                    fig.update_layout(
                        hovermode='x unified',
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📈 Current Prices")
                stocks_to_display = selected_stocks if selected_stocks else Config.STOCKS
                for stock in stocks_to_display:
                    stock_data = df[df["symbol"] == stock]
                    if not stock_data.empty and price_col:
                        latest_price = stock_data[price_col].iloc[-1]
                        prev_price = stock_data[price_col].iloc[-2] if len(stock_data) > 1 else latest_price
                        change = latest_price - prev_price
                        change_pct = (change / prev_price * 100) if prev_price > 0 else 0
                        
                        delta_color = "normal" if change >= 0 else "inverse"
                        st.metric(
                            label=stock,
                            value=f"${latest_price:.2f}",
                            delta=f"{change:+.2f} ({change_pct:+.2f}%)",
                            delta_color=delta_color
                        )
            
            # Volume analysis
            volume_col = "Volume" if "Volume" in df.columns else ("volume" if "volume" in df.columns else None)
            if volume_col:
                st.subheader("📊 Trading Volume")
                fig_volume = px.bar(
                    df,
                    x=datetime_col,
                    y=volume_col,
                    color="symbol",
                    title="Trading Volume by Stock",
                    labels={volume_col: "Volume", datetime_col: "Date"},
                    barmode='group'
                )
                st.plotly_chart(fig_volume, use_container_width=True)
            
            # Summary statistics
            if price_col:
                st.subheader("📋 Summary Statistics")
                summary_stats = df.groupby("symbol")[price_col].agg([
                    ("Current", "last"),
                    ("Min", "min"),
                    ("Max", "max"),
                    ("Avg", "mean"),
                    ("Std Dev", "std")
                ]).round(2)
                st.dataframe(summary_stats, use_container_width=True)
        else:
            # No symbol column - show all data or try to infer from file
            st.warning("⚠️ No symbol column found in data. Showing all available data.")
            st.info(f"Using file: {price_file}")
            st.info("💡 Tip: Run price streaming to get data with symbol column: `python -m src.streaming.stream_prices`")
            
            # Show basic price chart if Close column exists
            if price_col and datetime_col:
                st.subheader("📈 Price Chart (All Data)")
                fig = px.line(
                    df,
                    x=datetime_col,
                    y=price_col,
                    title="Price Chart",
                    labels={price_col: "Price ($)", datetime_col: "Date"}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show data preview
                st.subheader("📊 Data Preview")
                st.dataframe(df.head(20), use_container_width=True)
    else:
        st.error("❌ No price data files found")
        st.info("Please run the data collection scripts first:")
        st.code("python -m src.streaming.stream_prices")
        
        # Add button to run price streaming
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("🔄 Collect Price Data", use_container_width=True, type="primary"):
                with st.spinner("🔄 Collecting price data... This may take a moment."):
                    try:
                        import subprocess
                        import sys
                        from src.utils.config import Config
                        
                        # Run price collection (single run, not continuous stream)
                        from src.streaming.stream_prices import fetch_stock_price
                        import pandas as pd
                        from src.utils.helpers import save_csv
                        
                        symbols = st.session_state.get('selected_stocks', Config.STOCKS) or Config.STOCKS
                        all_prices = []
                        
                        # Ensure directories exist
                        os.makedirs("data/raw/prices", exist_ok=True)
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, symbol in enumerate(symbols):
                            status_text.text(f"Fetching data for {symbol}... ({i+1}/{len(symbols)})")
                            df = fetch_stock_price(symbol, period="5d")
                            if not df.empty:
                                all_prices.append(df)
                            progress_bar.progress((i + 1) / len(symbols))
                        
                        if all_prices:
                            combined_df = pd.concat(all_prices, ignore_index=True)
                            save_csv(combined_df, "data/raw/prices/historical_prices.csv")
                            
                            latest_prices = combined_df.groupby('symbol').tail(1)
                            save_csv(latest_prices, "data/raw/prices/latest_price.csv")
                            
                            st.success(f"✅ Successfully collected price data for {len(symbols)} stocks!")
                            st.info("🔄 Refreshing page to show updated data...")
                            st.rerun()
                        else:
                            st.error("❌ No price data was collected. Please check your internet connection and stock symbols.")
                    except Exception as e:
                        st.error(f"❌ Error collecting price data: {e}")
                        st.info("💡 Try running from terminal: `python -m src.streaming.stream_prices`")
        
        with col2:
            st.markdown("""
            **What this does:**
            - ✅ Fetches latest price data for selected stocks
            - ✅ Updates historical prices file
            - ✅ Creates latest price snapshot
            - ✅ Supports multi-stock data collection
            """)
        
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please ensure data files exist in the data/processed/features/ directory")
