import pickle

def save_model(model, label_names, model_path):
    payload = [model, label_names]
    with open(model_path, 'wb') as f:
        pickle.dump(payload, f)

def load_model(model_path):
    with open(model_path, 'rb') as f:
        payload = pickle.load(f)
    return payload
