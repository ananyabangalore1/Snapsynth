import cv2
import numpy as np
#from #paddleocr import PaddleOCR

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang="en")

def extract_text_and_layout(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Perform OCR to detect text and bounding boxes
    result = ocr.ocr(image_path, cls=True)

    html = "<html>\n<head>\n<style>\n"
    css = ""
    body = "<body>\n"

    # Loop through detected elements
    for line in result[0]:
        text = line[1][0]
        bounding_box = line[0]  # Coordinates of the detected text

        # Extract position and dimensions
        x_min = int(bounding_box[0][0])
        y_min = int(bounding_box[0][1])
        x_max = int(bounding_box[2][0])
        y_max = int(bounding_box[2][1])

        # Calculate width and height
        width = x_max - x_min
        height = y_max - y_min

        # Generate CSS for the detected text element
        class_name = f"text-{x_min}-{y_min}"
        css += f".{class_name} {{\n"
        css += f"  position: absolute;\n"
        css += f"  left: {x_min}px;\n"
        css += f"  top: {y_min}px;\n"
        css += f"  width: {width}px;\n"
        css += f"  height: {height}px;\n"
        css += f"  font-size: {int(height * 0.8)}px;\n"
        css += f"  color: black;\n"
        css += f"  text-align: center;\n"
        css += f"  line-height: {height}px;\n"
        css += "}\n"

        # Add HTML element
        body += f'<div class="{class_name}">{text}</div>\n'

    # Finalize HTML and CSS
    html += css
    html += "</style>\n</head>\n"
    html += body
    html += "</body>\n</html>"

    return html, css


# Path to your image
image_path = "path_to_your_image.jpg"

# Extract HTML and CSS from the image
html_output, css_output = extract_text_and_layout(image_path)

# Save HTML and CSS to files
with open("output.html", "w") as html_file:
    html_file.write(html_output)

with open("output.css", "w") as css_file:
    css_file.write(css_output)

print("HTML and CSS files have been generated!")
