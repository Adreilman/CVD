from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import sys
sys.path.append("features")
from ast_features import extract_features
from text_features import CodeTfidVectorizer
from scipy.sparse import hstack,csr_matrix
import numpy as np
import pandas as pd

app = FastAPI()

clf = joblib.load("models/classifier.pkl")
vec = joblib.load("models/tfidf_vectorizer.pkl")

class CodeRequest(BaseModel):
    code: str

@app.post("/predict")
def predict(request: CodeRequest):
    code = request.code
    ast_feat = pd.DataFrame([extract_features(code)])
    ast_sparse = csr_matrix(ast_feat.values)
    tfid_matrix = vec.transform([code])
    X = hstack([ast_sparse, tfid_matrix])
    prediction = clf.predict(X)[0]
    probabilities = clf.predict_proba(X)[0]
    confidence = np.max(probabilities)
    return {
        "prediction": prediction,
        "confidence": confidence,
    }
