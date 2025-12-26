import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# Ensure project root on sys.path for src.* imports
from streamlit_app import path_setup  # noqa: F401
from src.utils.config import Config

st.header("📰 News Sentiment Analysis")

# Get selected stocks from session state
selected_stocks = st.session_state.get('selected_stocks', [])

# Try to load news data with sentiment, or merge sentiment if available
news_files = [
    "data/raw/sentiment/sentiment_scores.csv",  # News with sentiment already included
    "data/raw/news/multisource_news.csv",
    "data/processed/merged/news_merged.csv",
    "data/raw/news/news_bs4.csv"
]

df = None
for file in news_files:
    if os.path.exists(file):
        try:
            df = pd.read_csv(file)
            # If this is sentiment_scores.csv, it already has sentiment
            # Otherwise, try to merge with sentiment data
            if "sentiment" not in df.columns and file != "data/raw/sentiment/sentiment_scores.csv":
                sentiment_file = "data/raw/sentiment/sentiment_scores.csv"
                if os.path.exists(sentiment_file):
                    try:
                        sentiment_df = pd.read_csv(sentiment_file)
                        # Merge on headline if available, or use index
                        if "headline" in df.columns and "headline" in sentiment_df.columns:
                            df = df.merge(
                                sentiment_df[["headline", "sentiment", "sentiment_score"]],
                                on="headline",
                                how="left"
                            )
                        else:
                            # Try to merge by index if headlines don't match
                            if len(df) == len(sentiment_df):
                                df["sentiment"] = sentiment_df["sentiment"].values
                                df["sentiment_score"] = sentiment_df["sentiment_score"].values
                    except Exception as e:
                        st.warning(f"Could not merge sentiment data: {e}")
            break
        except Exception as e:
            continue

if df is not None and not df.empty:
    # Filter by selected stocks
    if "symbol" in df.columns:
        stocks_to_filter = selected_stocks if selected_stocks else Config.STOCKS
        df = df[df["symbol"].isin(stocks_to_filter)]
    
    # Multi-stock sentiment comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Sentiment Distribution")
        if "sentiment" in df.columns:
            sentiment_count = df["sentiment"].value_counts().reset_index()
            sentiment_count.columns = ["sentiment", "count"]
            
            fig_pie = px.pie(
                sentiment_count,
                names="sentiment",
                values="count",
                title="Overall Sentiment Distribution",
                color_discrete_map={
                    "positive": "#00ff00",
                    "negative": "#ff0000",
                    "neutral": "#808080"
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("⚠️ Sentiment scores not available.")
            st.info("Run sentiment analysis to analyze news articles.")
            
            # Add button to run sentiment analysis
            if st.button("🔍 Run Sentiment Analysis", use_container_width=True):
                with st.spinner("Analyzing sentiment... This may take a moment."):
                    try:
                        from src.sentiment.sentiment_model import generate_sentiment
                        result_df = generate_sentiment()
                        if result_df is not None:
                            st.success("✅ Sentiment analysis completed! Refresh the page to see results.")
                            st.rerun()
                        else:
                            st.error("❌ Failed to run sentiment analysis. Check console for errors.")
                    except Exception as e:
                        st.error(f"❌ Error running sentiment analysis: {e}")
                        st.info("💡 Try running from terminal: `python run_sentiment_analysis.py`")
    
    with col2:
        st.subheader("📈 Sentiment by Stock")
        if "symbol" in df.columns and "sentiment" in df.columns:
            sentiment_by_stock = df.groupby(["symbol", "sentiment"]).size().reset_index(name="count")
            fig_bar = px.bar(
                sentiment_by_stock,
                x="symbol",
                y="count",
                color="sentiment",
                title="Sentiment Count by Stock",
                barmode='group',
                color_discrete_map={
                    "positive": "#00ff00",
                    "negative": "#ff0000",
                    "neutral": "#808080"
                }
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Source analysis
    if "source" in df.columns:
        st.subheader("📰 News Sources")
        source_count = df["source"].value_counts().reset_index()
        source_count.columns = ["source", "count"]
        
        fig_source = px.bar(
            source_count,
            x="source",
            y="count",
            title="Articles by Source",
            color="count",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_source, use_container_width=True)
    
    # Latest news articles
    st.subheader("📄 Latest News Articles")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        selected_stock_filter = st.selectbox(
            "Filter by Stock",
            options=["All"] + (selected_stocks if selected_stocks else Config.STOCKS),
            key="sentiment_stock_filter"
        )
    with col2:
        if "sentiment" in df.columns:
            sentiment_filter = st.selectbox(
                "Filter by Sentiment",
                options=["All", "positive", "negative", "neutral"],
                key="sentiment_filter"
            )
        else:
            sentiment_filter = "All"
    
    # Apply filters
    filtered_df = df.copy()
    if selected_stock_filter != "All":
        filtered_df = filtered_df[filtered_df["symbol"] == selected_stock_filter]
    if sentiment_filter != "All" and "sentiment" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["sentiment"] == sentiment_filter]
    
    # Display articles - only include columns that exist
    display_cols = []
    
    # Add columns in order of preference
    if "symbol" in filtered_df.columns:
        display_cols.append("symbol")
    if "headline" in filtered_df.columns:
        display_cols.append("headline")
    if "source" in filtered_df.columns:
        display_cols.append("source")
    if "sentiment" in filtered_df.columns:
        display_cols.append("sentiment")
    if "sentiment_score" in filtered_df.columns:
        display_cols.append("sentiment_score")
    if "url" in filtered_df.columns:
        display_cols.append("url")
    if "published_at" in filtered_df.columns:
        display_cols.append("published_at")
    
    # If no display columns found, show all available columns
    if not display_cols:
        display_cols = list(filtered_df.columns)
    
    # Filter to only show columns that exist
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    
    if available_cols:
        st.dataframe(
            filtered_df[available_cols].head(20),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No displayable columns found in the data.")
        st.info(f"Available columns: {list(filtered_df.columns)}")
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered News Data",
        data=csv,
        file_name=f"news_sentiment_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
else:
    st.warning("No news data found. Please run the multisource scraper first.")
    st.info("Run: `python src/scraping/multisource_scraper.py`")
    
    # Add button to run news scraper
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("📰 Scrape News Data", use_container_width=True, type="primary"):
            with st.spinner("📰 Scraping news from multiple sources... This may take a few minutes."):
                try:
                    import subprocess
                    import sys
                    from src.utils.config import Config
                    
                    symbols = st.session_state.get('selected_stocks', Config.STOCKS) or Config.STOCKS
                    
                    # Ensure directories exist
                    os.makedirs("data/raw/news", exist_ok=True)
                    os.makedirs("data/raw/sentiment", exist_ok=True)
                    
                    # Run the multisource scraper
                    from src.scraping.multisource_scraper import MultiSourceScraper
                    
                    scraper = MultiSourceScraper(symbols=symbols)
                    news_df = scraper.scrape_multiple_stocks(symbols=symbols, use_async=True)
                    
                    if news_df is not None and not news_df.empty:
                        scraper.save_results(news_df, "multisource_news.csv")
                        st.success(f"✅ Successfully scraped {len(news_df)} news articles!")
                        st.info("🔄 Refreshing page to show updated data...")
                        st.rerun()
                    else:
                        st.warning("⚠️ No news articles were scraped. Please check your internet connection.")
                except Exception as e:
                    st.error(f"❌ Error scraping news: {e}")
                    st.info("💡 Try running from terminal: `python src/scraping/multisource_scraper.py`")
    
    with col2:
        st.markdown("""
        **What this does:**
        - ✅ Scrapes news from multiple sources (Yahoo, Reuters, MarketWatch, etc.)
        - ✅ Collects articles for selected stocks
        - ✅ Saves data to multisource_news.csv
        - ✅ Supports async scraping for faster collection
        """)