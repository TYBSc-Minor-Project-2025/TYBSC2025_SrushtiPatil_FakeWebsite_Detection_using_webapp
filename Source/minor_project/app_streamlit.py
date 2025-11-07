# app_streamlit.py
import streamlit as st
import joblib
import pandas as pd
from utils import get_features_from_url

# Load the trained model, scaler, and training columns
model = joblib.load("phishing_model.pkl")
scaler = joblib.load("scaler.pkl")
training_columns = joblib.load("columns.pkl")

# App Title
st.title("🔍 Phishing Website Detection App")
st.write("Enter a website URL below to check if it’s **Fake (Phishing)** or **Legitimate** 👇")

# Input Box
url = st.text_input("Enter URL", "https://example.com")

# Predict Button
if st.button("Predict"):
    if not url.strip():
        st.error("⚠️ Please enter a valid URL.")
    else:
        # Extract features using your function
        features = get_features_from_url(url)

        # Convert to DataFrame (1-row)
        if isinstance(features, dict):
            features_df = pd.DataFrame([features])
        elif isinstance(features, pd.Series):
            features_df = features.to_frame().T
        else:
            features_df = features.copy()

        # Ensure same columns as model training
        for col in training_columns:
            if col not in features_df.columns:
                features_df[col] = 0
        features_df = features_df[training_columns]

        # Scale input features
        X_scaled = scaler.transform(features_df)

        # Predict (0 = Legitimate, 1 = Phishing)
        prediction = model.predict(X_scaled)[0]

        # Display the result
        if prediction == 1:
            st.markdown("### 🟥 **Result: Fake / Phishing**")
        else:
            st.markdown("### 🟩 **Result: Legitimate**")

        # Optional – show extracted features (remove if not needed)
        with st.expander("🔎 View Extracted Features"):
            st.dataframe(features_df.T)
