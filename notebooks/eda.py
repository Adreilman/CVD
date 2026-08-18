import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append("features")
from ast_features import extract_features
from text_features import CodeTfidVectorizer

df = pd.read_csv("data/processed/combined.csv")
print(len(df))
class_count = df["label"].value_counts()
plt.figure(figsize = (10,5))
sns.barplot(
    x = class_count.index,
    y = class_count.values
)

plt.xlabel("Class")
plt.ylabel("Number of samples")
plt.title("Class Distribution")
plt.xticks(rotation = 45)
plt.tight_layout()
plt.show()

ast_features = df["snippet"].apply(extract_features)
ast_df = pd.DataFrame(ast_features.tolist())
ast_df["label"] = df["label"].values
feature_cols = [c for c in ast_df.columns if c != "label"]
means = ast_df.groupby("label")[feature_cols].mean()
plt.figure(figsize = (10,6))
sns.heatmap(means, annot= True, fmt = ".2f", cmap = "rocket_r")
plt.title("Mean AST Feature Values by Class")
plt.xlabel("Features")
plt.ylabel("Classes")
plt.tight_layout()
plt.show()



PYTHON_STOPWORDS = [
    "def", "return", "import", "class", "self", "if", "else",
    "for", "in", "not", "and", "or", "True", "False", "None",
    "with", "as", "from", "pass", "raise", "try", "except"
]

vec = CodeTfidVectorizer(max_features = 500,stop_words = PYTHON_STOPWORDS)
X = vec.fit_transform(df["snippet"])
tfid_df = pd.DataFrame(X.toarray(), columns = vec.get_feature_names_out())
tfid_df["label"] = df["label"].values
for label in df["label"].unique():
    class_df = tfid_df[tfid_df["label"] == label].drop(columns = ["label"])
    top5 = class_df.mean().sort_values(ascending = False).head(5)
    print(f"\n{label}")
    print(top5)