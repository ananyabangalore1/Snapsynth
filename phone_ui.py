from PIL import Image, ImageDraw, ImageFont

def generate_phone_ui(df):
    # Create a blank phone-like image
    phone_outline = Image.new("RGB", (400, 800), "white")
    draw = ImageDraw.Draw(phone_outline)
    font = ImageFont.load_default()
    
    # Start drawing text on the phone outline
    y_offset = 50
    for index, row in df.iterrows():
        text = f"{row[0]}: {row[1]}"  # Use data from the Excel file (e.g., Column 1: Column 2)
        draw.text((50, y_offset), text, fill="black", font=font)
        y_offset += 30  # Adjust vertical spacing for text
    
    # Return the generated image
    return phone_outline
