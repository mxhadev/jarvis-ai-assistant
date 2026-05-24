import webbrowser
import subprocess
import urllib.parse
import pywhatkit
import time
import pyautogui
import time
from vision import analyze_screen


def open_website(url):

    webbrowser.open(url)

    return f"Opened {url}"


def open_vscode():

    subprocess.Popen("code")

    return "Opened VS Code"


def get_time():

    import time

    current_time = time.strftime("%I:%M %p")

    return f"The current time is {current_time}"


def youtube_search(query):

    encoded_query = urllib.parse.quote(query)

    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    open_website(url)

    return f"Searched YouTube for '{query}'"


def google_search(query):

    encoded_query = urllib.parse.quote(query)

    url = f"https://www.google.com/search?q={encoded_query}"

    open_website(url)

    return f"Searched Google for '{query}'"


def play_youtube(query):

    pywhatkit.playonyt(query)

    return f"Playing '{query}' on YouTube"
def type_text(text):

    pyautogui.write(
        text,
        interval=0.05
    )

    return f"Typed: {text}"


def press_key(key):

    pyautogui.press(key)

    return f"Pressed {key}"


def take_screenshot():

    filename = "screenshot.png"

    screenshot = pyautogui.screenshot()

    screenshot.save(filename)

    return f"Screenshot saved as {filename}"
def analyze_screen_tool():

    result = analyze_screen()

    return result