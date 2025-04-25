import easyocr
import cv2

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Cannot load image from {image_path}")
    results = reader.readtext(image)
    text = " ".join([text for (_, text, _) in results])
    return text
