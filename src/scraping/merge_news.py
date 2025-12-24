import pandas as pd
import glob

files = glob.glob("data/raw/news/*.csv")
df = pd.concat([pd.read_csv(f) for f in files])

df.drop_duplicates(subset=["headline"], inplace=True)
df.to_csv("data/processed/merged/news_merged.csv", index=False)
