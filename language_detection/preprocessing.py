import os
from bs4 import BeautifulSoup
import re

def clean_text(text):
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    return text

def tokenize(text):
    # Simple whitespace tokenization
    return text.split()

def preprocess_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    cleaned_text = clean_text(text)
    tokens = tokenize(cleaned_text)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(' '.join(tokens))

def preprocess_data(input_dir, output_dir):
    for lang in os.listdir(input_dir):
        lang_input_dir = os.path.join(input_dir, lang)
        lang_output_dir = os.path.join(output_dir, lang)
        os.makedirs(lang_output_dir, exist_ok=True)
        
        for filename in os.listdir(lang_input_dir):
            input_path = os.path.join(lang_input_dir, filename)
            output_path = os.path.join(lang_output_dir, filename.replace('.html', '.txt'))
            preprocess_file(input_path, output_path)

if __name__ == "__main__":
    input_dir = 'data/raw'
    output_dir = 'data/processed'
    preprocess_data(input_dir, output_dir)