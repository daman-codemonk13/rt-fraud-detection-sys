# 🛡️ Real-Time Fraud Detection System

A complete end-to-end pipeline for detecting fraudulent transactions in real time using machine learning, Kafka, Redis, and FastAPI.

---

## 📦 Project Structure

rt-fraud-detection-sys/
├── transactions.csv # Sample transaction data
├── train_model.py # Train the fraud detection model
├── inference_service.py # FastAPI service to serve predictions
├── real_time_api.py # Simulates sending transactions to Kafka
├── stream_simulator.py # Sends streaming transactions from CSV to Kafka
├── real_time_consumer.py # Kafka consumer to call inference on new transactions
├── feature_service.py # Fetches user-level features from Redis
├── generate_transactions.py # (Optional) Generate synthetic transactions
├── model.pkl # Trained XGBoost model
├── encoders.pkl # Saved categorical encoders
└── README.md # You're here



---

## ⚙️ Setup

### 1. 🔧 Prerequisites

- Python 3.9+
- Kafka
- Redis

Install dependencies:

```bash
pip install -r requirements.txt

Or manually:
pip install pandas scikit-learn xgboost fastapi uvicorn kafka-python redis joblib


🚀 How to Run (Full Pipeline)
Step 1: Start Kafka & Redis
Ensure Kafka and Redis are running locally.

# Start Kafka (Mac)
brew services start kafka
# Start Redis (Mac)
brew services start redis

Step 2: Train the Model
python train_model.py

This creates:

model.pkl: the trained XGBoost model

encoders.pkl: label encoders for categorical features

Step 3: Populate Redis Feature Store
python feature_service.py


Step 4: Start the Inference API
uvicorn inference_service:app --reload
Runs the FastAPI server at http://localhost:8000/infer/ to serve predictions.

Step 5: Start the Real-Time Kafka Consumer
python real_time_consumer.py
This listens to the Kafka topic and sends each message to the inference API.

Step 6: Stream Data into Kafka
python stream_simulator.py


🧠 Inference Format
POST request to http://localhost:8000/infer/

{
  "user_id": "user_001",
  "amount": 250,
  "device_id": "device_01",
  "location": "New York",
  "merchant_type": "grocery",
  "time_of_day": "afternoon",
  "num_txn_last_1hr": 5,
  "is_new_device": 0,
  "account_age_days": 100
}


✅ Example Output
{
  "fraud_probability": 0.01234
}

📊 Model
XGBoost classifier trained on encoded categorical + numeric features.

Features like location, merchant_type, user_id_freq, device_id_freq.

💡 Troubleshooting
Kafka connection errors: Make sure Kafka is running on localhost:9092.

Redis not responding: Restart Redis with brew services restart redis.

Feature mismatch: Ensure you include all columns expected during training.

Unseen categorical value: Encoder may fail on unknown categories unless handle_unknown="use_encoded_value" is set.


✍️ Author
Damanjot Singh
AI/ML Developer | Real-Time Systems

