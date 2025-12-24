"""
Regenerate ML predictions with symbol information
"""
from src.ml.predict import predict

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Regenerating ML Predictions with Symbol Information")
    print("=" * 60)
    predict()
    print("\n" + "=" * 60)
    print("✅ Done! Refresh your Streamlit app to see the updated predictions.")
    print("=" * 60)

