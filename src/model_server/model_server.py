import sklearn
import xgboost
import numpy as np
from redis_server import RedisServer
from utils import serialize_obj, deserialize_json, load_model

# Docker-compose internal DNS / network bridge resolves hostname 'redis_server' to the correct container
REDIS_HOST = 'redis_server'
REDIS_QUEUE_NAME = 'job_queue'
# REDIS_HOST = '0.0.0.0'
# REDIS_QUEUE_NAME = '0.0.0.0'

redis = RedisServer(host=REDIS_HOST, port=6379, db=0)

def test_run(xgb_model):
    '''
    Runs a single test case on script execution. Script will run only if test passes.

    Input: sklearn model
    '''
    test_example = np.array([[5.9, 3.2, 4.8, 1.8]])
    pred = xgb_model.predict(test_example)[0]

    print("Pred: {}. Pred label: {}".format(pred, label_names[pred]))
    assert pred == 1, "Loaded model does not predict correctly for test example"


def run():
    '''
    Model inference loop.
    Dequeues from Redis job queue and predicts.
    Enqueues prediction back into Redis job queue.
    '''
    # Redis look-up prediction loop
    while True:
        # Retrieve job from Redis, FIFO
        try:
            job = redis.dequeue('job_queue')
            job_obj = deserialize_json(job)
            job_id = job_obj['job_id']
            results = {}

            if 'data' in job_obj:
                # Model prediction
                data = job_obj['data']
                X = np.array([data])
                pred = int(xgb_model.predict(X)[0])
                results = {'predictions': {'prediction': pred, 'name': label_names[pred]}}
                print("Data {} Results {}".format(data, results))
            # Push prediction result to Redis
            redis.set(job_id, serialize_obj(results), expiry=300)

        except Exception as e:
            print("Unknown error occured. {}".format(e))
            continue

if __name__ == '__main__':
    model_path = '../../model/model.pkl'
    # Load model
    xgb_model, label_names = load_model(model_path)
    print("Loaded model: {}".format(xgb_model))
    print("Label names: {}".format(label_names))

    # Sanity check test run
    test_run(xgb_model)

    # Run model_server inference loop
    run()

# Test with
# curl -XPOST http://0.0.0.0:10000/api/predict -d'{"data": [5.9, 3.2, 4.8, 1.8]}' -H 'Content-Type: application/json'
# curl -XPOST http://0.0.0.0:10000/api/predict -d'{"data": [6.9, 3.1, 5.1, 2.3]}' -H 'Content-Type: application/json'
