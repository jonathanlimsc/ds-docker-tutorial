import time
from flask import Flask, jsonify, request
from redis_server import RedisServer
from utils import serialize_obj, deserialize_json, generate_uuid_string

MAX_TRIES = 100
SLEEP_DURATION = 0.1
REDIS_HOST = 'redis_server'
HTTP_HOST = 'http_server'

app = Flask(__name__)
redis = RedisServer(host=REDIS_HOST, port=6379, db=0)

@app.route('/api/predict', methods=['POST'])
def predict():
    '''
    Decorator function for /api/predict route.
    Takes in a JSON request with 'data' as key to an array of four floats:
    petal length, petal width, sepal length, sepal width
    Creates a job and enqueues into Redis, waits for it to be done up till MAX_TRIES

    Input: {'data': [float, float, float, float]}
    Returns: {'prediction': int, 'name': str}, int
    '''
    results = {'prediction': -1, 'name': 'nil'}
    response_code = 500

    # Generate a random UUID job id
    job_id = generate_uuid_string()

    try:
        # Retrieve data from request JSON
        data = request.json['data']

        # Create a job to put into Redis
        job = serialize_obj({'job_id': job_id, 'data': data})
        redis.enqueue('job_queue', job)

        response = None
        # Try to get done job from Redis
        for i in range(MAX_TRIES):
            done_job = redis.get(job_id)
            if done_job is not None:
                redis.delete(job_id)
                response = deserialize_json(done_job)
                break
            else:
                time.sleep(SLEEP_DURATION)

        # Return null response and server error
        if response is None:
            return jsonify(results), 500

        else:
            # Prediction server success
            if len(response.keys()) > 0:
                results = response['predictions']
                results = {'prediction': int(results['prediction']), 'name': results['name']}

            return jsonify(results), 200

    except Exception as e:
        print("Exception occurred {}".format(e))
        return jsonify(results), 500

if __name__ == '__main__':
    app.run(host=HTTP_HOST, port=10000, threaded=True)
