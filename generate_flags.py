from PIL import Image, ImageDraw, ImageFont
import os

def create_flag_image(country_code, emoji, output_path):
    # Create a new image with a white background
    img = Image.new('RGB', (60, 40), color='white')
    d = ImageDraw.Draw(img)
    
    # Use a font that supports emoji (you may need to adjust the path)
    font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 30)
    
    # Draw the emoji flag
    d.text((15, 5), emoji, font=font, fill=(0, 0, 0))
    
    # Save the image
    img.save(output_path)

# Ensure the flags directory exists
os.makedirs('static/flags', exist_ok=True)

# Create flag images
flags = {
    'en': '🇬🇧',
    'es': '🇪🇸',
    'fr': '🇫🇷',
    'tr': '🇹🇷',
    'it': '🇮🇹',
    'de': '🇩🇪'
}

for code, emoji in flags.items():
    create_flag_image(code, emoji, f'static/flags/{code}.png')

print("Flag images have been generated in the static/flags directory.")