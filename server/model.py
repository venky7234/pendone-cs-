import re
import string
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure NLTK resources are downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# List of words that might indicate fake news
SUSPICIOUS_WORDS = [
    'shocking', 'secret', 'conspiracy', 'hoax', 'shocking truth', 
    'they don\'t want you to know', 'miracle', 'cure', 'breakthrough',
    'amazing', 'incredible', 'exclusive', 'revealed', 'anonymous sources',
    'leaked', 'controversial', 'alarming', 'bombshell', 'unbelievable',
    'jaw-dropping', 'mind-blowing'
]

def preprocess_text(text):
    """
    Preprocess text by converting to lowercase, removing punctuation,
    and removing stopwords
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Join tokens back into a string
    processed_text = ' '.join(tokens)
    
    return processed_text

def extract_features(text):
    """
    Extract TF-IDF features from preprocessed text
    In a real implementation, this would use a pre-trained vectorizer
    """
    # In a real implementation, we would load a pre-trained vectorizer and model
    # For this example, we'll simulate the feature extraction
    
    # Simulate TF-IDF features
    words = text.split()
    feature_vector = np.zeros(100)  # Arbitrary feature size
    
    # Fill with some random values based on text length for demonstration
    for i in range(min(len(words), 100)):
        feature_vector[i] = 0.1 + 0.01 * len(words[i])
    
    return feature_vector

def predict_fake_news(features):
    """
    Predict if a news article is fake based on its features
    In a real implementation, this would use a pre-trained model
    """
    # In a real implementation, we would load and use a pre-trained model
    # For this example, we'll simulate a prediction based on basic heuristics
    
    # Simulate model prediction
    # For demonstration, we'll use a simple rule:
    # If the sum of features is above a threshold, classify as fake
    
    # This is just a placeholder for demonstration purposes
    feature_sum = np.sum(features)
    random_factor = np.random.random() * 0.3  # Add some randomness
    
    if feature_sum + random_factor > 5.0:
        return 'FAKE', 0.65 + random_factor
    else:
        return 'REAL', 0.70 + random_factor

def highlight_suspicious_phrases(text):
    """
    Identify and highlight potentially suspicious phrases in the text
    """
    highlights = []
    
    # Check for suspicious words/phrases
    for word in SUSPICIOUS_WORDS:
        for match in re.finditer(r'\b' + re.escape(word) + r'\b', text.lower()):
            # Calculate a suspicion score (higher = more suspicious)
            score = 0.5 + 0.3 * np.random.random()
            
            highlights.append({
                'start': match.start(),
                'end': match.end(),
                'score': score
            })
    
    # Add some random highlights for demonstration
    words = text.split()
    for i, word in enumerate(words):
        if len(word) > 5 and np.random.random() < 0.03:
            # Find position of this word in the original text
            # This is an approximation and might not be perfect
            word_pos = text.lower().find(word.lower())
            if word_pos != -1:
                highlights.append({
                    'start': word_pos,
                    'end': word_pos + len(word),
                    'score': 0.3 + 0.2 * np.random.random()  # Lower score for random words
                })
    
    return highlights