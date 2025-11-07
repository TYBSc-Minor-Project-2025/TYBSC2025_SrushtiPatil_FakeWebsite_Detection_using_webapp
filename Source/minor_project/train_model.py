# train_new_model.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from utils import get_features_from_url     # <-- same extractor your app uses

# === 1. Load any dataset that actually has raw URLs + label ===
# For now we’ll build our own small balanced dataset.
# Later you can replace this with a real phishing/legitimate URL list.
data = {
    "URL": [
        "https://www.google.com",
        "https://github.com",
        "https://www.wikipedia.org",
        "http://verify-paypal-login.com",
        "http://secure-login-update-account.g00gle.com",
        "http://amazon-login-security-check.ml",
        "http://paypal.com.login.verify.account-update.info",
        "http://microsoftsupport365.xyz"
    ],
    "CLASS_LABEL": [0, 0, 0, 1, 1, 1, 1, 1]   # 1 = phishing, 0 = legitimate
}
df = pd.DataFrame(data)

# === 2. Extract features using the same function as the app ===
print("🔧 Extracting features...")
features = []
for url in df["URL"]:
    feats = get_features_from_url(url)
    features.append(feats)

X = pd.DataFrame(features)
y = df["CLASS_LABEL"]
X = X.fillna(0)

print("Extracted feature columns:", X.columns.tolist())
print("Shape:", X.shape)

# === 3. Scale & Split ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.25, random_state=42, stratify=y
)

# === 4. Train ===
model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# === 5. Evaluate ===
y_pred = model.predict(X_test)
print("\nAccuracy:", round(accuracy_score(y_test, y_pred)*100, 2), "%")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Report:\n", classification_report(y_test, y_pred))

# === 6. Save ===
joblib.dump(model, "phishing_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(X.columns.tolist(), "columns.pkl")
print("\n💾 Model, scaler & columns saved successfully!")
