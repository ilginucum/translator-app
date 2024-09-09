import requests
import os

def download_wikipedia_sample(language, save_path):
    url = f"https://{language}.wikipedia.org/wiki/Special:Random"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Sample for {language} saved to {save_path}")
    else:
        print(f"Failed to download sample for {language}")

def collect_samples(languages, samples_per_language, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    for lang in languages:
        lang_dir = os.path.join(output_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        for i in range(samples_per_language):
            save_path = os.path.join(lang_dir, f"sample_{i+1}.html")
            download_wikipedia_sample(lang, save_path)

if __name__ == "__main__":
    languages = ['en', 'fr', 'es', 'de', 'it', 'tr']  # Add more languages as needed
    samples_per_language = 100
    output_dir = 'data/raw'
    
    collect_samples(languages, samples_per_language, output_dir)