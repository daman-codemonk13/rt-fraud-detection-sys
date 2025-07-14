# real_time_api.py
from fastapi import FastAPI
import joblib, redis
from kafka import KafkaConsumer, KafkaProducer
import pickle, json

app = FastAPI()
model = joblib.load("fraud_model.pkl")
redis_client = redis.Redis()
producer = KafkaProducer(bootstrap_servers="localhost:9092")

def enrich(t):
    features = pickle.loads(redis_client.get(f"user:{t['user_id']}"))
    return {**t, **features}

@app.post("/infer/")
def infer(transaction: dict):
    t = enrich(transaction)
    X = [t[k] for k in model.get_booster().feature_names]
    prob = float(model.predict_proba([X])[0][1])
    result = {"txn_id": t["txn_id"], "is_fraud": prob > 0.5, "score": prob}
    producer.send("fraud_decisions", json.dumps(result).encode())
    return result
