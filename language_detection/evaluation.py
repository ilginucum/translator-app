import sys
import os

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import joblib

try:
    from language_detection.model import LanguageDetectionModel
except ImportError:
    print("Error: Unable to import LanguageDetectionModel. Make sure the model.py file is in the correct location.")
    sys.exit(1)

def evaluate_model(model, X_test, y_test):
    y_pred = model.classifier.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(report)

if __name__ == "__main__":
    # Load the trained model
    model_path = os.path.join(parent_dir, 'models', 'language_detection_model.joblib')
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        sys.exit(1)

    model = joblib.load(model_path)

    # Load the features and languages
    features_path = os.path.join(parent_dir, 'models', 'tfidf_features.joblib')
    languages_path = os.path.join(parent_dir, 'models', 'languages.joblib')

    if not os.path.exists(features_path) or not os.path.exists(languages_path):
        print("Error: Required files (features or languages) not found.")
        sys.exit(1)

    features = joblib.load(features_path)
    languages = joblib.load(languages_path)

    # Split the data (use the same random_state as in training)
    _, X_test, _, y_test = train_test_split(features, languages, test_size=0.2, random_state=42)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)