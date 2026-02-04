# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from manipur_predictor import ManipurFloodPredictor

app = Flask(__name__)
predictor = ManipurFloodPredictor(
    model_path='manipur_flood_model.joblib',
    encoders_path='manipur_encoders.joblib'
)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    result = predictor.predict(**data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
