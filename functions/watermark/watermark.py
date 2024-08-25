from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

def add_watermark(input_folder, output_folder, watermark_text):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    font = ImageFont.truetype("arial.ttf", 200)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            img = Image.open(image_path)
            img = ImageOps.exif_transpose(img)  # Ensure correct orientation
            
            draw = ImageDraw.Draw(img)
            text_width, text_height = draw.textsize(watermark_text, font)
            width, height = img.size
            position = (width - text_width - 10, height - text_height - 10)

            draw.text(position, watermark_text, (255, 255, 255), font=font)
            
            output_path = os.path.join(output_folder, filename)
            img.save(output_path)

input_folder = 'functions/watermark/test'
output_folder = 'functions/watermark/test'
watermark_text = 'XM9G'

add_watermark(input_folder, output_folder, watermark_text)
