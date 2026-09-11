"""Flask API для предсказаний ML-модели."""
import pickle
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request


MODEL_PATH = Path('models/model.pkl')
FEATURE_NAMES = [
    'sepal length (cm)',
    'sepal width (cm)',
    'petal length (cm)',
    'petal width (cm)',
]

app = Flask(__name__)


def load_model():
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/predict', methods=['POST'])
def predict():
    model = load_model()
    data = request.get_json(force=True)
    features = pd.DataFrame([data['features']], columns=FEATURE_NAMES)
    prediction = model.predict(features).tolist()
    return jsonify({'prediction': prediction}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)