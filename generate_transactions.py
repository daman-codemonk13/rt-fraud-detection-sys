import pandas as pd
import numpy as np
import random

np.random.seed(42)

def generate_transaction(i):
    user_id = f"user_{random.randint(1, 100)}"
    device_id = f"device_{random.randint(1, 50)}"
    amount = round(np.random.exponential(scale=200), 2) + np.random.randint(5, 100)
    location = random.choice(["New York", "Chicago", "Miami", "San Francisco", "Dallas", "Seattle", "Boston"])
    merchant_type = random.choice(["grocery", "electronics", "food", "restaurant", "luxury", "banking", "ecommerce"])
    time_of_day = random.choice(["morning", "afternoon", "evening", "night"])
    num_txn_last_1hr = random.randint(0, 10)
    is_new_device = np.random.binomial(1, 0.2)
    account_age_days = np.random.randint(1, 1000)

    # Heuristic: fraud more likely if high amount, new device, or high txn freq
    fraud_score = 0
    if amount > 1000: fraud_score += 1
    if is_new_device: fraud_score += 1
    if num_txn_last_1hr > 5: fraud_score += 1
    if account_age_days < 30: fraud_score += 1

    is_fraud = 1 if fraud_score >= 2 and random.random() < 0.8 else 0

    return {
        "txn_id": f"tx_{i+1}",
        "user_id": user_id,
        "amount": amount,
        "device_id": device_id,
        "location": location,
        "merchant_type": merchant_type,
        "time_of_day": time_of_day,
        "num_txn_last_1hr": num_txn_last_1hr,
        "is_new_device": is_new_device,
        "account_age_days": account_age_days,
        "is_fraud": is_fraud
    }

# Generate 500 transactions
data = [generate_transaction(i) for i in range(500)]
df = pd.DataFrame(data)
df.to_csv("transactions.csv", index=False)

print("✅ transactions.csv with 500 records generated.")
