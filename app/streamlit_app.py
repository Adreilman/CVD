import streamlit as st
import joblib
import sys
sys.path.append("features")
from ast_features import extract_features
from text_features import CodeTfidVectorizer
from scipy.sparse import hstack, csr_matrix
import numpy as np
import pandas as pd

clf = joblib.load("models/classifier.pkl")
vec = joblib.load("models/tfidf_vectorizer.pkl")

st.title("PyVulnDetector")
st.subheader("ML-based Python Code Vulnerability Detector")
code_input = st.text_area("Enter your Python Code snippet here:\n", height = 200, placeholder = "Check your vulnerability")

if st.button("Check Vulnerability"):
    if code_input.strip() == "":
        st.warning("Please enter the code")
    else:
        ast_feat = pd.DataFrame([extract_features(code_input)])
        ast_sparse = csr_matrix(ast_feat.values)
        tfid_matrix = vec.transform([code_input])
        X = hstack([ast_sparse, tfid_matrix])
        prediction = clf.predict(X)[0]
        probabilites = clf.predict_proba(X)[0]
        confidence = np.max(probabilites)
        CONFIDENCE_THRESHOLD = 0.75
        if prediction == "safe":
            st.success(f"Safe - No vulnerability detected ({confidence:.0%} confidence)")
        elif confidence < CONFIDENCE_THRESHOLD:
            st.warning(f"Uncertain — possible {prediction} ({confidence:.0%} confidence, low confidence prediction)")
        else:
            st.error(f"Vulnerable {prediction} - Potential vulnerability detected ({confidence:.0%} confidence)")
        proba_df = pd.DataFrame({
        "Class": clf.classes_,
        "Confidence": clf.predict_proba(X)[0]
        })
        st.bar_chart(proba_df.set_index("Class"))

