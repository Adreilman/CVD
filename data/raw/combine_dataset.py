import pandas as pd

seed_df = pd.read_csv("data/processed/seed_snippets.csv")
hf_df = pd.read_csv("data/processed/hf_snippets.csv")

combined_df = pd.concat([seed_df, hf_df], ignore_index=True)

combined_df = combined_df.drop_duplicates(subset="snippet")
safe_df = combined_df[combined_df["label"] == "Safe"].sample(n=600, random_state=42)
vuln_df = combined_df[combined_df["label"] != "Safe"]
combined_df = pd.concat([safe_df, vuln_df], ignore_index=True)

print(combined_df["label"].value_counts())
combined_df.to_csv("data/processed/combined.csv", index=False)
print("Combined dataset saved")
print(combined_df.head())