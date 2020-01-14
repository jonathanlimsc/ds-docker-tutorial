import pickle
import json
import uuid
import os

def generate_uuid_string():
    return str(uuid.uuid4())

def serialize_obj(obj):
    return json.dumps(obj)

def deserialize_json(json_str, encoding='utf-8'):
    return json.loads(json_str.decode(encoding))

def save_model(model, label_names, model_path):
    payload = [model, label_names]
    with open(model_path, 'wb') as f:
        pickle.dump(payload, f)

def load_model(model_path):
    with open(model_path, 'rb') as f:
        payload = pickle.load(f)
    return payload
