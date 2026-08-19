# PyVulnDetect

ML-based Python code vulnerability detector using AST structural features 
and TF-IDF text features with a Random Forest classifier.

## What it does
Detects 5 vulnerability types in Python code snippets:
- CWE-89: SQL Injection
- CWE-78: OS Command Injection
- CWE-502: Insecure Deserialization
- CWE-79: XSS
- Safe (no vulnerability detected)

## Tech Stack
- Python 3.x
- scikit-learn (Random Forest, TF-IDF)
- pandas, numpy
- Streamlit (web app)
- Hugging Face `datasets` (data pipeline)

## Project Structure
CVD/
├── data/
│ ├── raw/ # download + seed dataset scripts
│ └── processed/ # combined.csv (generated)
├── features/
│ ├── ast_features.py # AST-based structural features
│ └── text_features.py # TF-IDF code tokenizer
├── models/
│ └── train.py # training pipeline
├── notebooks/
│ └── eda.py # exploratory data analysis
└── app/
└── streamlit_app.py # Streamlit web app


## How to Run
```bash
# 1. create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash

# 2. install dependencies
pip install -r requirements.txt

# 3. generate seed dataset
python data/raw/make_seed_dataset.py

# 4. download and filter HF dataset
python data/raw/download_hf_dataset.py

# 5. merge datasets
python data/raw/combine_datasets.py

# 6. train the model
python models/train.py

# 7. run the app
streamlit run app/streamlit_app.py
```

## Model Performance
- Overall accuracy: 80%
- Best class: SAFE  (F1: 0.86)
- Weakest class: CWE-78(F1: 0.56)

## Known Limitations
- Short generic snippets can produce low-confidence uncertain predictions
- XSS detection is weak — AST features don't cover HTML rendering patterns well
- CWE-798 (Hardcoded Credentials) was dropped from v1 due to insufficient training data (8 examples)
- Safe code that uses risky function names (e.g. `cursor.execute` with parameterized queries) can be misclassified

## Dataset
- Primary: `ayshajavd/code-security-vulnerability-dataset` (Hugging Face) — filtered to Python + 5 target CWEs
- Supplementary: hand-crafted synthetic seed dataset (`data/raw/make_seed_dataset.py`)