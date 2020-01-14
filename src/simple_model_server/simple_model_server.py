import sklearn
import xgboost
import numpy as np
from flask import Flask, jsonify, request
from utils import load_model

app = Flask(__name__)

def test_run(xgb_model):
    '''
    Runs a single test case on script execution. Script will run only if test passes.

    Input: sklearn model
    '''
    test_example = np.array([[5.9, 3.2, 4.8, 1.8]])
    pred = xgb_model.predict(test_example)[0]

    print("Pred: {}. Pred label: {}".format(pred, label_names[pred]))
    assert pred == 1, "Loaded model does not predict correctly for test example"

@app.route('/api/predict', methods=['POST'])
def predict():
    '''
    Decorator function for /api/predict route.
    Takes in a JSON request with 'data' as key to an array of four floats:
    petal length, petal width, sepal length, sepal width

    Input: {'data': [float, float, float, float]}
    Returns: {'prediction': int, 'name': str}, int
    '''
    results = {'prediction': -1, 'name': 'nil'}

    try:
        # Retrieve data from request JSON
        data = request.json['data']

        # Generate prediction from model
        X = np.array([data])
        pred = xgb_model.predict(X)[0]
        results = {'prediction': int(pred), 'name': label_names[pred]}
    except Exception as e:
        print("Exception occured: {}".format(e))
        return jsonify(results), 500

    return jsonify(results), 200

if __name__ == '__main__':
    model_path = '../../model/model.pkl'
    # Load model
    xgb_model, label_names = load_model(model_path)
    print("Loaded model: {}".format(xgb_model))
    print("Label names: {}".format(label_names))

    # Sanity check test run
    test_run(xgb_model)

    # Run Flask app
    app.run(host='0.0.0.0', port=10000, threaded=True)

# Test with
# curl -XPOST http://0.0.0.0:10000/api/predict -d'{"data": [5.9, 3.2, 4.8, 1.8]}' -H 'Content-Type: application/json'
# curl -XPOST http://0.0.0.0:10000/api/predict -d'{"data": [6.9, 3.1, 5.1, 2.3]}' -H 'Content-Type: application/json'
