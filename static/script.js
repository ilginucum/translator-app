document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('translate-form');
    const inputText = document.getElementById('input-text');
    const sourceLang = document.getElementById('source-lang');
    const targetLang = document.getElementById('target-lang');
    const resultArea = document.getElementById('result');
    const detectedLanguage = document.getElementById('detected-language');
    const loadingIndicator = document.getElementById('loading');
    const stickman = document.getElementById('stickman');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        // Show loading indicator
        loadingIndicator.style.display = 'block';
        resultArea.value = '';
        detectedLanguage.textContent = '';

        fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'text': inputText.value,
                'source_lang': sourceLang.value,
                'target_lang': targetLang.value
            })
        })
        .then(response => response.json())
        .then(data => {
            resultArea.value = data.translated_text;
            if (data.detected_language) {
                detectedLanguage.textContent = `Detected language: ${data.detected_language}`;
                animateStickman(data.detected_language);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultArea.value = 'An error occurred during translation.';
        })
        .finally(() => {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
        });
    });

    function animateStickman(detectedLang) {
        const stickman = document.getElementById('stickman');
        const targetFlag = document.querySelector(`.flag[data-lang="${detectedLang}"]`);
        
        if (targetFlag) {
            const flagRect = targetFlag.getBoundingClientRect();
            const containerRect = document.getElementById('animation-container').getBoundingClientRect();
            const targetPosition = flagRect.left - containerRect.left;
    
            // Start running animation
            stickman.style.animationPlayState = 'running';
    
            // Move stickman to the flag
            stickman.style.left = `${targetPosition}px`;
    
            // Stop running animation when reached the flag
            stickman.addEventListener('transitionend', function() {
                stickman.style.animationPlayState = 'paused';
            }, { once: true });
        }
    }
});