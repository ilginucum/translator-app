import os
import sys
from flask import Flask, render_template, request, jsonify
import requests
import joblib

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the LanguageDetectionModel class
from language_detection.model import LanguageDetectionModel

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(current_dir, 'models', 'language_detection_model.joblib')
if os.path.exists(model_path):
    model = joblib.load(model_path)
    print("Model loaded successfully")
else:
    print(f"Error: Model file not found at {model_path}")
    model = None

# Define all supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'tr': 'Turkish'
}

def detect_language(text):
    if model is None:
        return "Model not loaded"
    return model.predict(text)

@app.route('/')
def index():
    return render_template('index.html', languages=SUPPORTED_LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    source_lang = request.form['source_lang']
    target_lang = request.form['target_lang']

    # If source language is not provided, detect it
    if not source_lang:
        source_lang = detect_language(text)

    # Call MyMemory API for translation
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
    response = requests.get(url)
    data = response.json()
    translated_text = data['responseData']['translatedText']

    return jsonify({
        'translated_text': translated_text,
        'detected_language': source_lang if not request.form['source_lang'] else None
    })

if __name__ == '__main__':
    app.run(debug=True)