import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Ensure project root on sys.path for src.* imports
from streamlit_app import path_setup  # noqa: F401
from src.utils.config import Config

st.header("💰 Company Financial Statements")

# Get selected stocks from session state
selected_stocks = st.session_state.get('selected_stocks', [])

# Statement type selector
statement_type = st.radio(
    "Select Financial Statement",
    ["Income Statement", "Balance Sheet", "Cash Flow Statement"],
    horizontal=True
)

# Load appropriate statement
base_path = "data/raw/fundamentals/"
statement_files = {
    "Income Statement": f"{base_path}income_statement.csv",
    "Balance Sheet": f"{base_path}balance_sheet.csv",
    "Cash Flow Statement": f"{base_path}cash_flow.csv"
}

file_path = statement_files.get(statement_type)

if file_path and os.path.exists(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Filter by selected stocks
        if "symbol" in df.columns:
            stocks_to_filter = selected_stocks if selected_stocks else Config.STOCKS
            df = df[df["symbol"].isin(stocks_to_filter)]
        
        # Stock selector for detailed view
        selected_stock = st.selectbox(
            "Select Stock for Detailed View",
            options=selected_stocks if selected_stocks else Config.STOCKS,
            key="fundamentals_stock"
        )
        
        stock_df = df[df["symbol"] == selected_stock] if "symbol" in df.columns else df
        
        if not stock_df.empty:
            # Key metrics visualization
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"📊 {statement_type} - {selected_stock}")
                
                # Find key columns based on statement type
                if statement_type == "Income Statement":
                    key_cols = ["Total Revenue", "Operating Income", "Net Income", "Gross Profit"]
                elif statement_type == "Balance Sheet":
                    key_cols = ["Total Assets", "Total Liabilities", "Stockholders Equity", "Cash"]
                else:  # Cash Flow
                    key_cols = ["Operating Cash Flow", "Free Cash Flow", "Capital Expenditure", "Net Income"]
                
                # Filter available columns
                available_cols = [col for col in key_cols if col in stock_df.columns]
                
                if available_cols and "Date" in stock_df.columns:
                    # Prepare data for visualization
                    plot_df = stock_df[["Date"] + available_cols].copy()
                    plot_df = plot_df.set_index("Date")
                    
                    # Convert to numeric, handling any string values
                    for col in available_cols:
                        plot_df[col] = pd.to_numeric(plot_df[col], errors='coerce')
                    
                    # Create line chart
                    fig = go.Figure()
                    for col in available_cols:
                        fig.add_trace(go.Scatter(
                            x=plot_df.index,
                            y=plot_df[col],
                            mode='lines+markers',
                            name=col
                        ))
                    
                    fig.update_layout(
                        title=f"{statement_type} Trends - {selected_stock}",
                        xaxis_title="Date",
                        yaxis_title="Amount ($)",
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📈 Key Metrics Comparison")
                
                # Multi-stock comparison for key metrics
                stocks_to_compare = selected_stocks if selected_stocks else Config.STOCKS
                if available_cols and len(stocks_to_compare) > 1:
                    comparison_df = df[df["symbol"].isin(stocks_to_compare)]
                    if "Date" in comparison_df.columns:
                        latest_date = comparison_df["Date"].max()
                        latest_data = comparison_df[comparison_df["Date"] == latest_date]
                        
                        if not latest_data.empty:
                            for col in available_cols[:3]:  # Show top 3 metrics
                                if col in latest_data.columns:
                                    metric_df = latest_data[["symbol", col]].copy()
                                    metric_df[col] = pd.to_numeric(metric_df[col], errors='coerce')
                                    
                                    fig_bar = px.bar(
                                        metric_df,
                                        x="symbol",
                                        y=col,
                                        title=col,
                                        color="symbol"
                                    )
                                    st.plotly_chart(fig_bar, use_container_width=True)
            
            # Full statement table
            st.subheader("📋 Full Statement Data")
            
            # Format numeric columns for display
            display_df = stock_df.copy()
            numeric_cols = display_df.select_dtypes(include=['float64', 'int64']).columns
            for col in numeric_cols:
                if col not in ["Date", "symbol", "statement_type", "scraped_at"]:
                    display_df[col] = display_df[col].apply(
                        lambda x: f"${x:,.0f}" if pd.notna(x) and abs(x) >= 1 else f"${x:,.2f}" if pd.notna(x) else "N/A"
                    )
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Download button
            csv = stock_df.to_csv(index=False)
            st.download_button(
                label=f"📥 Download {statement_type} Data",
                data=csv,
                file_name=f"{statement_type.lower().replace(' ', '_')}_{selected_stock}.csv",
                mime="text/csv"
            )
        else:
            st.warning(f"No data available for {selected_stock}")
    except Exception as e:
        st.error(f"Error loading financial data: {e}")
        st.info("Please ensure the financial statements have been scraped")
else:
    st.warning(f"{statement_type} data file not found.")
    st.info("Please run the financial statements scraper first:")
    st.code("python src/scraping/financial_statements_scraper.py")
    
    # Add button to run financial statements scraper
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("💰 Scrape Financial Statements", use_container_width=True, type="primary"):
            with st.spinner("💰 Scraping financial statements... This may take a few minutes."):
                try:
                    from src.utils.config import Config
                    from src.scraping.financial_statements_scraper import FinancialStatementsScraper
                    
                    # Ensure directories exist
                    os.makedirs("data/raw/fundamentals", exist_ok=True)
                    
                    symbols = st.session_state.get('selected_stocks', Config.STOCKS) or Config.STOCKS
                    
                    scraper = FinancialStatementsScraper(symbols=symbols)
                    statements = scraper.scrape_multiple_stocks(use_async=True)
                    
                    if statements:
                        scraper.save_statements(statements)
                        st.success("✅ Successfully scraped financial statements!")
                        st.info("🔄 Refreshing page to show updated data...")
                        st.rerun()
                    else:
                        st.warning("⚠️ No financial statements were scraped. Please check your internet connection.")
                except Exception as e:
                    st.error(f"❌ Error scraping financial statements: {e}")
                    st.info("💡 Try running from terminal: `python src/scraping/financial_statements_scraper.py`")
    
    with col2:
        st.markdown("""
        **What this does:**
        - ✅ Scrapes Income Statement, Balance Sheet, and Cash Flow
        - ✅ Collects historical financial data
        - ✅ Saves data for all selected stocks
        - ✅ Supports async scraping for faster collection
        """)