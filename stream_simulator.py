# stream_simulator.py
from kafka import KafkaProducer
import json, time, pandas as pd

producer = KafkaProducer(bootstrap_servers="localhost:9092")
df = pd.read_csv("transactions.csv")

for _, row in df.sample(frac=0.1).iterrows():
    txn = row.drop("is_fraud").to_dict()
    producer.send("txn_stream", json.dumps(txn).encode())
    time.sleep(0.1)
