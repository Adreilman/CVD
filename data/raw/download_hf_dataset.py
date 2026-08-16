"""
Downloads ayshajavd/code-security-vulnerability-dataset from Hugging Face
and filters it down to:
    - Python snippets only
    - Your 5 target CWE classes + Safe

Confirmed schema (from the dataset card):
    code            str   - source code snippet
    code_fixed      str   - secure version, when available
    cwe_id          str   - e.g. "CWE-89", or "safe"
    owasp           str   - OWASP Top 10 2021 category, or "safe"
    language        str   - "Python", "C", "JavaScript", "Java", "PHP", "Go", "C++", ...
    source          str   - which underlying dataset it came from (bigvul, labeled_dataset, etc.)
    is_vulnerable   bool
    labels          list[int]  - 31-dim multi-label vector (index 0 = safe)

Setup:
    pip install datasets pandas

Usage:
    python data/raw/download_hf_dataset.py
"""
import pandas as pd
from datasets import load_dataset

# Maps this dataset's cwe_id values to the label names used in our
# seed_snippets.csv, so the two can be concatenated directly.
TARGET_CWE_MAP = {
    "CWE-89": "CWE-89_SQLi",
    "CWE-78": "CWE-78_CmdInjection",
    "CWE-502": "CWE-502_InsecureDeser",
    "CWE-798": "CWE-798_HardcodedCreds",
    "CWE-79": "CWE-79_XSS",
}
SAFE_LABEL = "Safe"

print("Downloading dataset from Hugging Face (~132MB, first run may take a while)...")
ds = load_dataset("ayshajavd/code-security-vulnerability-dataset")
print(ds)

# Combine all three splits before re-filtering/re-splitting ourselves --
# we want our own train/val/test split once we know how much Python data
# survives the CWE filter (the original split was over 175k rows across
# many languages, so our subset ratio may differ).
df = pd.concat([
    ds["train"].to_pandas(),
    ds["validation"].to_pandas(),
    ds["test"].to_pandas(),
], ignore_index=True)
print(f"\nTotal rows across all splits: {len(df)}")

# ---------------------------------------------------------------
# Filter 1: Python only
# ---------------------------------------------------------------
df_py = df[df["language"].str.lower() == "python"].copy()
print(f"Python-only rows: {len(df_py)}")
print("\nPython rows by cwe_id:")
print(df_py["cwe_id"].value_counts())

# ---------------------------------------------------------------
# Filter 2: our 5 target CWEs + safe, normalize label names
# ---------------------------------------------------------------
def map_label(cwe_value: str):
    if pd.isna(cwe_value) or str(cwe_value).strip().lower() == "safe":
        return SAFE_LABEL
    return TARGET_CWE_MAP.get(str(cwe_value).strip(), None)

df_py["mapped_label"] = df_py["cwe_id"].apply(map_label)
df_filtered = df_py.dropna(subset=["mapped_label"]).copy()

df_final = pd.DataFrame({
    "snippet": df_filtered["code"],
    "label": df_filtered["mapped_label"],
    "source": "ayshajavd_hf_" + df_filtered["source"].astype(str),
})

# Drop exact duplicate snippets (common in commit-mined datasets)
before = len(df_final)
df_final = df_final.drop_duplicates(subset="snippet")
print(f"\nDropped {before - len(df_final)} exact-duplicate snippets")

print("\nFinal filtered class distribution:")
print(df_final["label"].value_counts())

out_path = "data/processed/hf_snippets.csv"
df_final.to_csv(out_path, index=False)
print(f"\nSaved {len(df_final)} rows to {out_path}")

print("\nIf any class comes back very small or missing, that's expected --")
print("this dataset only has Python examples where the underlying source")
print("dataset ('labeled_dataset', 'cybernative_dpo', etc.) happened to")
print("include Python. Check the per-class counts above before training;")
print("you may need to lean on the synthetic seed set or drop a sparse")
print("class rather than train on 3-4 examples.")

print("\nNext step -- merge with your seed set:")
print("  import pandas as pd")
print("  seed = pd.read_csv('data/processed/seed_snippets.csv')")
print("  hf = pd.read_csv('data/processed/hf_snippets.csv')")
print("  pd.concat([seed, hf], ignore_index=True).to_csv('data/processed/combined.csv', index=False)")