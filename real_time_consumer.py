# real_time_consumer.py
from kafka import KafkaConsumer
import json, requests

consumer = KafkaConsumer("txn_stream", bootstrap_servers="localhost:9092")
for msg in consumer:
    txn = json.loads(msg.value)
    resp = requests.post("http://localhost:8000/infer/", json=txn)
    print(resp.json())
