import pandas as pd
import numpy as np
from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append("features")
from ast_features import extract_features
from text_features import CodeTfidVectorizer



df = pd.read_csv("data/processed/combined.csv")
# print(f"Loaded {len(df)} rows")
# print(df["label"].value_counts())
df = df[df["label"] != "CWE-798_HardcodedCreds"]
ast_df = pd.DataFrame(df["snippet"].apply(extract_features).tolist())
print(ast_df.shape)

PYTHON_STOPWORDS = [
    "def", "return", "import", "class", "self", "if", "else","for", "in", "not", "and", "or", "True", "False", "None","with", "as", "from", "pass", "raise", "try", "except"
]
vec = CodeTfidVectorizer(max_features = 500,stop_words = PYTHON_STOPWORDS)
tfid_matrix = vec.fit_transform(df["snippet"])
print(tfid_matrix.shape)

ast_sparse = csr_matrix(ast_df.values)
X = hstack([ast_sparse, tfid_matrix])
print(X.shape)
Y = np.array(df["label"].tolist())

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size = 0.2, random_state = 42,stratify = Y)

print(f"Train:{X_train.shape}, Test:{X_test.shape}")

clf = RandomForestClassifier(n_estimators = 100, class_weight = "balanced", random_state = 42)
clf.fit(X_train,Y_train)
print(f"Test Accuracy: {clf.score(X_test,Y_test)}")
print(f"Trained. Number of Trees: {clf.n_estimators}")

Y_pred = clf.predict(X_test)
print(classification_report(Y_test, Y_pred))

cm = confusion_matrix(Y_test, Y_pred, labels = clf.classes_)
plt.figure(figsize = (8,6))
sns.heatmap(cm, annot = True, fmt = "d",
            xticklabels = clf.classes_, yticklabels = clf.classes_, cmap = "Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.xticks(rotation = 45)
plt.tight_layout()
plt.show()


import joblib

joblib.dump(clf, "models/classifier.pkl")
joblib.dump(vec, "models/tfidf_vectorizer.pkl")
print("Model saved to models/")