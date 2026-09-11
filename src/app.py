"""Flask API для предсказаний ML-модели BankNote Authentication."""
import pickle
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request


MODEL_PATH = Path('models/model.pkl')
FEATURE_NAMES = ['variance', 'skewness', 'curtosis', 'entropy']

app = Flask(__name__)


def load_model():
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)


HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>BankNote Authentication</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        h1 { color: #333; }
        label { display: block; margin: 15px 0 5px; font-weight: bold; }
        input { width: 100%; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { margin-top: 20px; padding: 12px 30px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; border-radius: 4px; font-size: 18px; }
        .authentic { background: #d4edda; color: #155724; }
        .fake { background: #f8d7da; color: #721c24; }
        .error { background: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <h1>BankNote Authentication</h1>
    <p>Введите признаки банкноты для проверки подлинности.</p>
    <form id="predict-form">
        <label for="variance">Variance</label>
        <input type="number" step="any" id="variance" value="2.3718" required>

        <label for="skewness">Skewness</label>
        <input type="number" step="any" id="skewness" value="7.4908" required>

        <label for="curtosis">Curtosis</label>
        <input type="number" step="any" id="curtosis" value="0.015989" required>

        <label for="entropy">Entropy</label>
        <input type="number" step="any" id="entropy" value="-1.7414" required>

        <button type="submit">Проверить</button>
    </form>
    <div id="result"></div>

    <script>
        document.getElementById('predict-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const features = [
                parseFloat(document.getElementById('variance').value),
                parseFloat(document.getElementById('skewness').value),
                parseFloat(document.getElementById('curtosis').value),
                parseFloat(document.getElementById('entropy').value),
            ];
            const resultDiv = document.getElementById('result');

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({features}),
                });
                const data = await response.json();
                const pred = data.prediction[0];
                const isAuthentic = pred === 0;

                resultDiv.className = 'result ' + (isAuthentic ? 'authentic' : 'fake');
                resultDiv.innerHTML = isAuthentic
                    ? 'Банкнота <b>подлинная</b> (класс 0)'
                    : 'Банкнота <b>поддельная</b> (класс 1)';
            } catch (err) {
                resultDiv.className = 'result error';
                resultDiv.textContent = 'Ошибка: ' + err.message;
            }
        });
    </script>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    """Веб-форма для тестирования модели."""
    return HTML_PAGE, 200, {'Content-Type': 'text/html; charset=utf-8'}


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
