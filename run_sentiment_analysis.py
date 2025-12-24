"""
Quick script to run sentiment analysis on news data
"""
from src.sentiment.sentiment_model import generate_sentiment

if __name__ == "__main__":
    print("=" * 60)
    print("📰 Running Sentiment Analysis on News Data")
    print("=" * 60)
    generate_sentiment()
    print("\n" + "=" * 60)
    print("✅ Done! Refresh your Streamlit app to see the results.")
    print("=" * 60)

