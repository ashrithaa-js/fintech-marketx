"""
Setup script for Streamlit Cloud deployment
Creates necessary directories and sample data files
"""
import os
from pathlib import Path

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        "data/raw/prices",
        "data/raw/news",
        "data/raw/sentiment",
        "data/raw/fundamentals",
        "data/processed/features",
        "data/logs",
        "powerbi/data_sources",
        ".streamlit"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_sample_files():
    """Create sample data files for Streamlit Cloud"""
    # Create empty sample files
    sample_files = [
        "data/processed/features/features.csv",
        "data/processed/features/predictions.csv",
        "data/raw/news/multisource_news.csv",
        "data/raw/sentiment/sentiment_scores.csv",
        "data/raw/fundamentals/income_statement.csv",
        "data/raw/fundamentals/balance_sheet.csv",
        "data/raw/fundamentals/cash_flow.csv",
        "data/raw/prices/historical_prices.csv"
    ]
    
    for file_path in sample_files:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(file_path):
            # Create empty file with header
            with open(file_path, 'w') as f:
                f.write("")  # Empty file
            print(f"✓ Created sample file: {file_path}")

if __name__ == "__main__":
    print("Setting up directories and sample files for Streamlit Cloud...")
    create_directories()
    create_sample_files()
    print("\n✅ Setup complete!")

