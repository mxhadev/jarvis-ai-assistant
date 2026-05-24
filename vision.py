import pyautogui
import pytesseract
import requests

from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def capture_screen():

    screenshot = pyautogui.screenshot()

    filename = "vision_screenshot.png"

    screenshot.save(filename)

    return filename


def extract_screen_text():

    image_path = capture_screen()

    image = Image.open(image_path)

    extracted_text = pytesseract.image_to_string(image)

    return extracted_text.strip()


def analyze_screen():

    screen_text = extract_screen_text()

    if not screen_text:

        return "I could not detect anything meaningful on the screen."

    prompt = f"""
You are Jarvis vision system.

Your task is to understand and summarize what is visible on the user's computer screen.

SCREEN TEXT:
{screen_text}

Instructions:
- Ignore broken OCR text
- Ignore random symbols
- Infer the likely app/page/content
- Give a clean human-style summary
- Be concise
- Speak naturally

Example:
"The user is on YouTube watching music videos."

Summary:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()["response"]

    return result.strip()