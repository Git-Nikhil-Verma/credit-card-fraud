import os
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Get the absolute path of the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Absolute paths for the model and PCA transformer
model_path = os.path.join(current_directory, 'files', 'credit_card_fraud_model.pkl')
pca_path = os.path.join(current_directory, 'files', 'pca_transformer.pkl')

# Load the pre-trained model and PCA transformer
try:
    model = joblib.load(model_path)
    pca = joblib.load(pca_path)
    print("✅ Model and PCA transformer loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model or PCA transformer: {e}")
    model = None
    pca = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or pca is None:
        print("⚠️ Model or PCA transformer is not loaded properly.")
        return jsonify({'error': 'Model or PCA transformer is not loaded properly.'}), 500

    try:
        # Get input data from the POST request
        data = request.json
        print("📥 Received data:", data)

        # Validate that all required keys are present
        required_keys = [f'V{i}' for i in range(1, 29)] + ['Amount', 'Time']
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            print(f"❌ Missing required keys: {missing_keys}")
            return jsonify({'error': f'Missing input fields: {", ".join(missing_keys)}'}), 400

        # Ensure all values are numeric
        try:
            data = {key: float(value) for key, value in data.items()}
        except ValueError as ve:
            print(f"❌ Non-numeric values in input: {ve}")
            return jsonify({'error': 'All input values must be numeric.'}), 400

        # Convert the data into a DataFrame (single row)
        input_data = pd.DataFrame([data])
        print(f"📋 Input data converted to DataFrame: {input_data}")

        # Apply PCA transformation
        try:
            print(f"🔄 Input data shape before PCA: {input_data.shape}")
            input_transformed = pca.transform(input_data)
            print(f"🔄 Data after PCA transformation: {input_transformed}")
        except Exception as e:
            print(f"❌ Error during PCA transformation: {e}")
            return jsonify({'error': 'Error during PCA transformation.'}), 500

        # Make a prediction
        prediction = model.predict(input_transformed)
        print(f"✅ Prediction: {prediction}")

        # Return the prediction as a JSON response
        return jsonify({'prediction': int(prediction[0])})

    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return jsonify({'error': 'Error during prediction. Check server logs for details.'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
