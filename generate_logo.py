import os
from PIL import Image, ImageDraw, ImageFont

def generate_logo():
    # Create a 512x512 canvas with dark blue background matching brandBlue
    img = Image.new('RGBA', (512, 512), color=(2, 6, 23, 255))
    draw = ImageDraw.Draw(img)
    
    # Outer circle matching brandGreen (#10b981)
    draw.ellipse([20, 20, 492, 492], fill=None, outline=(16, 185, 129, 255), width=24)
    
    # Inner dashed-style circle with deep blue tone
    draw.ellipse([45, 45, 467, 467], fill=None, outline=(29, 78, 216, 255), width=8)
    
    # Couple / athletic fitness silhouettes representational shapes inside
    # Male silhouette
    draw.ellipse([210, 140, 302, 232], fill=(16, 185, 129, 255))
    draw.polygon([(210, 232), (302, 232), (322, 340), (190, 340)], fill=(16, 185, 129, 230))
    
    # Female silhouette
    draw.ellipse([210, 160, 290, 240], fill=(29, 78, 216, 255))
    draw.polygon([(210, 240), (290, 240), (305, 340), (195, 340)], fill=(29, 78, 216, 230))
    
    # Elegant central dumbbells shapes
    draw.rectangle([160, 220, 352, 236], fill=(16, 185, 129, 255))
    draw.ellipse([140, 210, 164, 246], fill=(29, 78, 216, 255))
    draw.ellipse([348, 210, 372, 246], fill=(29, 78, 216, 255))
    
    # Save the output image as logo.png
    img.save('logo.png', 'PNG')
    print("FitHarmony logo.png successfully generated!")

if __name__ == '__main__':
    generate_logo()
