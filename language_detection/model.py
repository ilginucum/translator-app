import os
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

class LanguageDetectionModel:
    def __init__(self):
        self.vectorizer = None
        self.classifier = MultinomialNB()

    def train(self, features, languages):
        X_train, X_test, y_train, y_test = train_test_split(features, languages, test_size=0.2, random_state=42)
        self.classifier.fit(X_train, y_train)
        return X_test, y_test

    def predict(self, text):
        if self.vectorizer is None:
            raise ValueError("Vectorizer is not loaded. Call load_vectorizer() first.")
        features = self.vectorizer.transform([text])
        return self.classifier.predict(features)[0]

    def load_vectorizer(self, vectorizer_path):
        self.vectorizer = joblib.load(vectorizer_path)

    def save(self, model_path):
        joblib.dump(self, model_path)

    @classmethod
    def load(cls, model_path):
        return joblib.load(model_path)

if __name__ == "__main__":
    # Check if the required files exist
    if not os.path.exists('models/tfidf_features.joblib') or not os.path.exists('models/languages.joblib'):
        print("Error: Required files not found. Please run feature_extraction.py first.")
        exit(1)

    # Load the features and languages
    features = joblib.load('models/tfidf_features.joblib')
    languages = joblib.load('models/languages.joblib')

    # Create and train the model
    model = LanguageDetectionModel()
    X_test, y_test = model.train(features, languages)

    # Load the vectorizer
    model.load_vectorizer('models/tfidf_vectorizer.joblib')

    # Create the 'models' directory if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # Save the trained model
    model.save('models/language_detection_model.joblib')

    print("Model trained and saved successfully.")