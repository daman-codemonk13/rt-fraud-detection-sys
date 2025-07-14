# feature_service.py
import redis, pickle

r = redis.Redis()
def get_user_features(user_id):
    raw = r.get(f"user:{user_id}")
    return pickle.loads(raw) if raw else {}