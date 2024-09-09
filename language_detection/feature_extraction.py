import os
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def load_data(data_dir):
    texts = []
    languages = []
    
    for lang in os.listdir(data_dir):
        lang_dir = os.path.join(data_dir, lang)
        for filename in os.listdir(lang_dir):
            with open(os.path.join(lang_dir, filename), 'r', encoding='utf-8') as file:
                texts.append(file.read())
                languages.append(lang)
    
    return texts, languages

def extract_features(texts, max_features=5000):
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3), max_features=max_features)
    features = vectorizer.fit_transform(texts)
    
    return vectorizer, features

if __name__ == "__main__":
    data_dir = 'data/processed'
    texts, languages = load_data(data_dir)
    
    vectorizer, features = extract_features(texts)
    
    # Create the 'models' directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save the vectorizer and features
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.joblib')
    joblib.dump(features, 'models/tfidf_features.joblib')
    joblib.dump(languages, 'models/languages.joblib')
    
    print(f"Extracted features shape: {features.shape}")
    print(f"Number of samples: {len(languages)}")
    print("Vectorizer and features saved successfully.")