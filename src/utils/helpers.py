import pandas as pd
from src.utils.logger import log

def save_csv(df, path):
    df.to_csv(path, index=False)
    log(f"Saved file: {path}")

def load_csv(path):
    log(f"Loaded file: {path}")
    return pd.read_csv(path)
