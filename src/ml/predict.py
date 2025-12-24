"""
Enhanced ML Prediction Script
Generates predictions with symbol information from historical prices
"""
import joblib
import pandas as pd
import os
from src.utils.logger import get_logger
from src.utils.config import Config

logger = get_logger(__name__)


def predict():
    """Generate predictions for stock prices"""
    try:
        # Load model
        if not os.path.exists("model.pkl"):
            logger.error("Model file not found. Please train the model first.")
            print("[ERROR] Model file (model.pkl) not found.")
            print("[INFO] Run: python -m src.ml.train_model")
            return
        
        model = joblib.load("model.pkl")
        logger.info("Model loaded successfully")
        
        # Try to load features.csv
        features_file = "data/processed/features/features.csv"
        if not os.path.exists(features_file):
            logger.error(f"Features file not found: {features_file}")
            print(f"[ERROR] Features file not found: {features_file}")
            print("[INFO] Run feature engineering first")
            return
        
        df = pd.read_csv(features_file)
        logger.info(f"Loaded {len(df)} records from features.csv")
        
        # Prepare features for prediction
        X = df.drop(columns=["target"], errors="ignore")
        
        # Generate predictions
        predictions = model.predict(X)
        df["prediction"] = predictions
        
        # Convert regression predictions to binary (UP/DOWN) if needed
        # Threshold: > 0.5 = UP (1), <= 0.5 = DOWN (0)
        if predictions.dtype in ['float64', 'float32']:
            df["prediction_binary"] = (predictions > 0.5).astype(int)
            df["prediction_label"] = df["prediction_binary"].map({1: "UP", 0: "DOWN"})
        else:
            # Already binary
            df["prediction_binary"] = predictions
            df["prediction_label"] = df["prediction_binary"].map({1: "UP", 0: "DOWN"})
        
        # Add confidence score
        try:
            if hasattr(model, "predict_proba"):
                # Classification model
                proba = model.predict_proba(X)
                df["confidence"] = proba.max(axis=1)
            else:
                # Regression model - calculate confidence based on prediction distance from threshold
                # Predictions closer to 0 or 1 are more confident
                df["confidence"] = abs(predictions - 0.5) * 2  # Scale to 0-1
        except:
            # Fallback confidence calculation
            if predictions.dtype in ['float64', 'float32']:
                df["confidence"] = abs(predictions - 0.5) * 2
            else:
                df["confidence"] = 0.7
        
        # Try to merge with historical prices to get symbol and datetime
        historical_file = "data/raw/prices/historical_prices.csv"
        if os.path.exists(historical_file):
            try:
                historical_df = pd.read_csv(historical_file)
                
                # If historical data has symbol and datetime, try to merge
                if "symbol" in historical_df.columns and "Datetime" in historical_df.columns:
                    # Match by index or by Close price
                    if "Close" in df.columns and "Close" in historical_df.columns:
                        # Merge on Close price (approximate match)
                        historical_df = historical_df.sort_values("Datetime").reset_index(drop=True)
                        df = df.reset_index(drop=True)
                        
                        # Add symbol and datetime from historical if lengths match
                        if len(df) <= len(historical_df):
                            # Take the most recent records
                            historical_subset = historical_df.tail(len(df)).reset_index(drop=True)
                            df["symbol"] = historical_subset["symbol"].values
                            df["datetime"] = pd.to_datetime(historical_subset["Datetime"]).values
                            df["price"] = historical_subset["Close"].values
                            df["predicted_price"] = df["Close"] * (1 + df["prediction"] * 0.01)  # Approximate
                        else:
                            # Use the latest stock from historical
                            latest_symbol = historical_df["symbol"].iloc[-1] if len(historical_df) > 0 else Config.STOCKS[0]
                            df["symbol"] = latest_symbol
                            df["datetime"] = pd.to_datetime("now")
                            df["price"] = df["Close"] if "Close" in df.columns else 0
                            df["predicted_price"] = df["Close"] * (1 + df["prediction"] * 0.01) if "Close" in df.columns else 0
                    else:
                        # Fallback: use first stock from config
                        df["symbol"] = Config.STOCKS[0] if Config.STOCKS else "AAPL"
                        df["datetime"] = pd.to_datetime("now")
                        df["price"] = df["Close"] if "Close" in df.columns else 0
                        df["predicted_price"] = df["Close"] * (1 + df["prediction"] * 0.01) if "Close" in df.columns else 0
                else:
                    # No symbol in historical, use default
                    df["symbol"] = Config.STOCKS[0] if Config.STOCKS else "AAPL"
                    df["datetime"] = pd.to_datetime("now")
                    df["price"] = df["Close"] if "Close" in df.columns else 0
                    df["predicted_price"] = df["Close"] * (1 + df["prediction"] * 0.01) if "Close" in df.columns else 0
            except Exception as e:
                logger.warning(f"Could not merge with historical prices: {e}")
                # Fallback: add default symbol
                df["symbol"] = Config.STOCKS[0] if Config.STOCKS else "AAPL"
                df["datetime"] = pd.to_datetime("now")
                df["price"] = df["Close"] if "Close" in df.columns else 0
                df["predicted_price"] = df["Close"] * (1 + df["prediction"] * 0.01) if "Close" in df.columns else 0
        else:
            # No historical file, add default values
            logger.warning("Historical prices file not found. Using default symbol.")
            df["symbol"] = Config.STOCKS[0] if Config.STOCKS else "AAPL"
            df["datetime"] = pd.to_datetime("now")
            df["price"] = df["Close"] if "Close" in df.columns else 0
            df["predicted_price"] = df["Close"] * (1 + df["prediction"] * 0.01) if "Close" in df.columns else 0
        
        # Save predictions
        output_file = "data/processed/features/predictions.csv"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
        
        logger.info(f"Predictions saved to {output_file}")
        print("Predictions generated successfully!")
        print(f"Total predictions: {len(df)}")
        if "symbol" in df.columns:
            symbols = df["symbol"].unique()
            print(f"Stocks: {', '.join(symbols)}")
        
    except Exception as e:
        logger.error(f"Error generating predictions: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    predict()
