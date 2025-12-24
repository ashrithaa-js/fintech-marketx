"""
Enhanced Sentiment Analysis for Multi-Source News
Analyzes sentiment from multiple news sources and categorizes as positive/negative/neutral
"""
from textblob import TextBlob
import pandas as pd
import os
from src.utils.helpers import save_csv
from src.utils.logger import get_logger
from src.sentiment.preprocess_text import clean_text

logger = get_logger(__name__)


def sentiment_score(text):
    """Calculate sentiment polarity score (-1 to 1)"""
    if pd.isna(text) or not text or len(str(text).strip()) == 0:
        return 0.0
    try:
        return TextBlob(str(text)).sentiment.polarity
    except Exception as e:
        logger.warning(f"Error calculating sentiment for text: {e}")
        return 0.0


def categorize_sentiment(score):
    """Categorize sentiment score into positive, negative, or neutral"""
    if score > 0.1:
        return "positive"
    elif score < -0.1:
        return "negative"
    else:
        return "neutral"


def generate_sentiment(news_file=None):
    """
    Generate sentiment scores for news articles
    
    Args:
        news_file: Path to news CSV file. If None, tries multiple sources.
    """
    # Try multiple news file sources
    if news_file is None:
        news_files = [
            "data/raw/news/multisource_news.csv",
            "data/raw/news/news_bs4.csv",
            "data/raw/news/news_selenium.csv",
            "data/processed/merged/news_merged.csv"
        ]
        
        df = None
        for file_path in news_files:
            if os.path.exists(file_path):
                try:
                    df = pd.read_csv(file_path)
                    logger.info(f"Loaded news data from: {file_path}")
                    break
                except Exception as e:
                    logger.warning(f"Error loading {file_path}: {e}")
                    continue
        
        if df is None or df.empty:
            logger.error("No news data files found!")
            print("❌ No news data files found. Please run the news scraper first:")
            print("   python -m src.scraping.multisource_scraper")
            return
    else:
        if not os.path.exists(news_file):
            logger.error(f"News file not found: {news_file}")
            return
        df = pd.read_csv(news_file)
    
    # Check if headline column exists
    if "headline" not in df.columns:
        logger.error("No 'headline' column found in news data")
        print(f"❌ Available columns: {df.columns.tolist()}")
        return
    
    logger.info(f"Processing sentiment for {len(df)} news articles...")
    
    # Clean and calculate sentiment
    df["clean_headline"] = df["headline"].apply(clean_text)
    df["sentiment_score"] = df["clean_headline"].apply(sentiment_score)
    df["sentiment"] = df["sentiment_score"].apply(categorize_sentiment)
    
    # Save results
    output_dir = "data/raw/sentiment"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "sentiment_scores.csv")
    save_csv(df, output_file)
    
    # Print summary
    sentiment_counts = df["sentiment"].value_counts()
    logger.info(f"Sentiment analysis completed!")
    logger.info(f"Positive: {sentiment_counts.get('positive', 0)}")
    logger.info(f"Negative: {sentiment_counts.get('negative', 0)}")
    logger.info(f"Neutral: {sentiment_counts.get('neutral', 0)}")
    
    print(f"\n✅ Sentiment analysis completed!")
    print(f"📊 Results saved to: {output_file}")
    print(f"\n📈 Sentiment Distribution:")
    print(f"   Positive: {sentiment_counts.get('positive', 0)}")
    print(f"   Negative: {sentiment_counts.get('negative', 0)}")
    print(f"   Neutral: {sentiment_counts.get('neutral', 0)}")
    
    return df


if __name__ == "__main__":
    generate_sentiment()
