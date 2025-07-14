# train_model.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score

# Load data
df = pd.read_csv("transactions.csv")

# Encode categorical columns
categorical_cols = ["location", "merchant_type", "time_of_day"]
encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
df[categorical_cols] = encoder.fit_transform(df[categorical_cols])

# Feature engineering (example)
df["user_id_freq"] = df["user_id"].map(df["user_id"].value_counts())
df["device_id_freq"] = df["device_id"].map(df["device_id"].value_counts())

# Drop unused cols
X = df.drop(columns=["is_fraud", "txn_id", "user_id", "device_id"])
y = df["is_fraud"]

# Train-test split
X_train, X_val, y_train, y_val = train_test_split(X, y, stratify=y, test_size=0.2)

# Train model
model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict_proba(X_val)[:, 1]
roc_score = roc_auc_score(y_val, y_pred)
print(f"Validation ROC AUC: {roc_score:.4f}")

# Save model and encoder
joblib.dump(model, "fraud_model.pkl")
joblib.dump(encoder, "encoders.pkl")
