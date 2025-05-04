from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
import pickle
import numpy as np
from model import predict_fake_news, preprocess_text, extract_features, highlight_suspicious_phrases

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze text for fake news detection
    """
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({'error': 'Empty text provided'}), 400
        
        # Preprocess the text
        processed_text = preprocess_text(text)
        
        # Extract features
        features = extract_features(processed_text)
        
        # Make prediction
        prediction, confidence = predict_fake_news(features)
        
        # Generate highlights for suspicious phrases
        highlights = highlight_suspicious_phrases(text)
        
        # Return the result
        return jsonify({
            'prediction': prediction,
            'confidence': confidence,
            'highlights': highlights
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)