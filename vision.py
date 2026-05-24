import pyautogui
import pytesseract
import requests
import cv2
import numpy as np

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


def click_text(target_text):

    screenshot = pyautogui.screenshot()

    image = np.array(screenshot)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT
    )

    for i, text in enumerate(data["text"]):

        clean_target = target_text.lower().replace(" ", "")

        clean_text = text.lower().replace(" ", "")

        if clean_target in clean_text:

            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            center_x = x + w // 2
            center_y = y + h // 2

            pyautogui.moveTo(
                center_x,
                center_y,
                duration=0.3
            )

            pyautogui.click()

            return f"Clicked on {target_text}"

    return f"Could not find {target_text} on screen."