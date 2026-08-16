import pandas as pd

df = pd.read_csv("data/processed/combined.csv")
print(len(df))
print(df["label"].value_counts())

