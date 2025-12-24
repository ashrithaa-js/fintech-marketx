"""
Enhanced Dynamic PowerBI Data Exporter
Exports processed data in formats compatible with PowerBI
Supports real-time updates, scheduled refreshes, and dynamic data model
"""
import pandas as pd
import os
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from src.utils.logger import get_logger
from src.utils.config import Config

logger = get_logger(__name__)


class PowerBIExporter:
    """Dynamic PowerBI data exporter"""
    
    def __init__(self, output_dir: str = "powerbi/data_sources"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_to_csv(self, df: pd.DataFrame, filename: str, symbol: Optional[str] = None):
        """Export DataFrame to CSV for PowerBI"""
        if df.empty:
            logger.warning(f"No data to export for {filename}")
            return
        
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=False)
        logger.info(f"Exported {len(df)} rows to {filepath}")
    
    def export_stock_prices(self, symbols: List[str] = None):
        """Export stock price data for PowerBI"""
        try:
            price_file = "data/processed/features/features.csv"
            if os.path.exists(price_file):
                df = pd.read_csv(price_file)
                
                if symbols:
                    df = df[df['symbol'].isin(symbols)]
                
                # Add PowerBI-friendly columns
                if 'datetime' in df.columns:
                    df['date'] = pd.to_datetime(df['datetime']).dt.date
                    df['year'] = pd.to_datetime(df['datetime']).dt.year
                    df['month'] = pd.to_datetime(df['datetime']).dt.month
                    df['quarter'] = pd.to_datetime(df['datetime']).dt.quarter
                
                self.export_to_csv(df, "stock_prices.csv")
            else:
                logger.warning(f"Price file not found: {price_file}")
        except Exception as e:
            logger.error(f"Error exporting stock prices: {e}")
    
    def export_news_sentiment(self, symbols: List[str] = None):
        """Export news and sentiment data for PowerBI"""
        try:
            news_file = "data/raw/news/multisource_news.csv"
            sentiment_file = "data/raw/sentiment/sentiment_scores.csv"
            
            # Export news
            if os.path.exists(news_file):
                df_news = pd.read_csv(news_file)
                if symbols:
                    df_news = df_news[df_news['symbol'].isin(symbols)]
                
                # Add date columns
                if 'published_at' in df_news.columns:
                    df_news['date'] = pd.to_datetime(df_news['published_at']).dt.date
                    df_news['year'] = pd.to_datetime(df_news['published_at']).dt.year
                    df_news['month'] = pd.to_datetime(df_news['published_at']).dt.month
                
                self.export_to_csv(df_news, "news_data.csv")
            
            # Export sentiment
            if os.path.exists(sentiment_file):
                df_sentiment = pd.read_csv(sentiment_file)
                if symbols:
                    df_sentiment = df_sentiment[df_sentiment['symbol'].isin(symbols)]
                
                self.export_to_csv(df_sentiment, "sentiment_data.csv")
        except Exception as e:
            logger.error(f"Error exporting news/sentiment: {e}")
    
    def export_financial_statements(self, symbols: List[str] = None):
        """Export financial statements for PowerBI"""
        try:
            base_path = "data/raw/fundamentals/"
            statements = ['income_statement', 'balance_sheet', 'cash_flow']
            
            for stmt in statements:
                filepath = f"{base_path}{stmt}.csv"
                if os.path.exists(filepath):
                    df = pd.read_csv(filepath)
                    
                    if symbols and 'symbol' in df.columns:
                        df = df[df['symbol'].isin(symbols)]
                    
                    # Add date columns if Date column exists
                    if 'Date' in df.columns:
                        df['date'] = pd.to_datetime(df['Date']).dt.date
                        df['year'] = pd.to_datetime(df['Date']).dt.year
                    
                    self.export_to_csv(df, f"{stmt}_powerbi.csv")
        except Exception as e:
            logger.error(f"Error exporting financial statements: {e}")
    
    def export_ml_predictions(self, symbols: List[str] = None):
        """Export ML predictions for PowerBI"""
        try:
            predictions_file = "data/processed/features/predictions.csv"
            if os.path.exists(predictions_file):
                df = pd.read_csv(predictions_file)
                
                if symbols and 'symbol' in df.columns:
                    df = df[df['symbol'].isin(symbols)]
                
                # Add date columns
                if 'datetime' in df.columns:
                    df['date'] = pd.to_datetime(df['datetime']).dt.date
                    df['year'] = pd.to_datetime(df['datetime']).dt.year
                    df['month'] = pd.to_datetime(df['datetime']).dt.month
                
                self.export_to_csv(df, "ml_predictions.csv")
        except Exception as e:
            logger.error(f"Error exporting ML predictions: {e}")
    
    def export_all_data(self, symbols: List[str] = None):
        """Export all available data for PowerBI"""
        logger.info("Starting PowerBI data export...")
        
        self.export_stock_prices(symbols)
        self.export_news_sentiment(symbols)
        self.export_financial_statements(symbols)
        self.export_ml_predictions(symbols)
        
        logger.info("PowerBI data export completed!")
    
    def create_data_model_summary(self, symbols: List[str] = None):
        """Create a comprehensive summary document for PowerBI data model with relationships"""
        symbols = symbols or Config.STOCKS
        
        summary = {
            "export_date": datetime.now().isoformat(),
            "symbols": symbols,
            "refresh_schedule": "Recommended: Every 15 minutes during market hours",
            "tables": [
                {
                    "name": "stock_prices",
                    "description": "Historical stock price data with technical indicators",
                    "key_columns": ["symbol", "date", "price", "volume"],
                    "primary_key": ["symbol", "date"],
                    "relationships": [
                        {"to_table": "ml_predictions", "on": ["symbol", "date"]},
                        {"to_table": "sentiment_data", "on": ["symbol", "date"]}
                    ]
                },
                {
                    "name": "news_data",
                    "description": "Multi-source news articles",
                    "key_columns": ["symbol", "source", "headline", "date"],
                    "primary_key": ["headline", "symbol"],
                    "relationships": [
                        {"to_table": "sentiment_data", "on": ["headline", "symbol"]}
                    ]
                },
                {
                    "name": "sentiment_data",
                    "description": "Sentiment scores for news articles",
                    "key_columns": ["symbol", "sentiment_score", "date"],
                    "primary_key": ["symbol", "date"],
                    "relationships": [
                        {"to_table": "stock_prices", "on": ["symbol", "date"]}
                    ]
                },
                {
                    "name": "income_statement_powerbi",
                    "description": "Company income statements",
                    "key_columns": ["symbol", "Date", "Total Revenue", "Net Income"],
                    "primary_key": ["symbol", "Date"],
                    "relationships": [
                        {"to_table": "balance_sheet_powerbi", "on": ["symbol", "Date"]},
                        {"to_table": "cash_flow_powerbi", "on": ["symbol", "Date"]}
                    ]
                },
                {
                    "name": "balance_sheet_powerbi",
                    "description": "Company balance sheets",
                    "key_columns": ["symbol", "Date", "Total Assets", "Total Liabilities"],
                    "primary_key": ["symbol", "Date"],
                    "relationships": [
                        {"to_table": "income_statement_powerbi", "on": ["symbol", "Date"]}
                    ]
                },
                {
                    "name": "cash_flow_powerbi",
                    "description": "Company cash flow statements",
                    "key_columns": ["symbol", "Date", "Operating Cash Flow", "Free Cash Flow"],
                    "primary_key": ["symbol", "Date"],
                    "relationships": [
                        {"to_table": "income_statement_powerbi", "on": ["symbol", "Date"]}
                    ]
                },
                {
                    "name": "ml_predictions",
                    "description": "ML model predictions for stock prices",
                    "key_columns": ["symbol", "date", "predicted_price", "confidence"],
                    "primary_key": ["symbol", "date"],
                    "relationships": [
                        {"to_table": "stock_prices", "on": ["symbol", "date"]}
                    ]
                }
            ],
            "measures": [
                {
                    "name": "Total Market Cap",
                    "formula": "SUM(stock_prices[price] * stock_prices[volume])",
                    "description": "Total market capitalization across selected stocks"
                },
                {
                    "name": "Average Sentiment Score",
                    "formula": "AVERAGE(sentiment_data[sentiment_score])",
                    "description": "Average sentiment score for selected stocks"
                },
                {
                    "name": "Prediction Accuracy",
                    "formula": "COUNTROWS(FILTER(ml_predictions, ml_predictions[confidence] > 0.7)) / COUNTROWS(ml_predictions)",
                    "description": "Percentage of high-confidence predictions"
                }
            ]
        }
        
        summary_path = os.path.join(self.output_dir, "data_model_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Created comprehensive data model summary at {summary_path}")
        return summary
    
    def create_refresh_script(self, refresh_interval_minutes: int = 15):
        """Create a PowerShell script for automated PowerBI data refresh"""
        script_content = f"""# PowerBI Data Refresh Script
# This script can be scheduled to run every {refresh_interval_minutes} minutes using Windows Task Scheduler

$python = "python"
$script = "{os.path.abspath(__file__)}"
$logFile = "{os.path.join(self.output_dir, 'refresh_log.txt')}"

Write-Host "Starting PowerBI data refresh at $(Get-Date)" | Tee-Object -FilePath $logFile -Append
& $python $script --refresh
Write-Host "Refresh completed at $(Get-Date)" | Tee-Object -FilePath $logFile -Append
"""
        
        script_path = os.path.join(self.output_dir, "refresh_data.ps1")
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        logger.info(f"Created refresh script at {script_path}")
        return script_path
    
    def export_with_timestamp(self, symbols: List[str] = None):
        """Export all data with timestamp for versioning"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.output_dir, f"backup_{timestamp}")
        os.makedirs(backup_dir, exist_ok=True)
        
        # Temporarily change output directory
        original_dir = self.output_dir
        self.output_dir = backup_dir
        
        try:
            self.export_all_data(symbols)
            self.create_data_model_summary(symbols)
        finally:
            self.output_dir = original_dir
        
        logger.info(f"Exported timestamped backup to {backup_dir}")


if __name__ == "__main__":
    import sys
    
    exporter = PowerBIExporter()
    symbols = Config.STOCKS
    
    if "--refresh" in sys.argv:
        logger.info("Running scheduled refresh...")
        exporter.export_all_data(symbols=symbols)
        exporter.create_data_model_summary(symbols=symbols)
    else:
        exporter.export_all_data(symbols=symbols)
        exporter.create_data_model_summary(symbols=symbols)
        exporter.create_refresh_script(refresh_interval_minutes=15)
        print(f"\n✓ PowerBI data exported successfully!")
        print(f"✓ Data model summary created")
        print(f"✓ Refresh script created")
        print(f"\nTo schedule automatic refreshes, add a Windows Task Scheduler job:")
        print(f"  Action: powershell.exe")
        print(f"  Arguments: -File {exporter.output_dir}/refresh_data.ps1")

