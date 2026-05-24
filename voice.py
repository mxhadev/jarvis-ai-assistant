import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import os
import time


# -----------------------------
# SPEAK FUNCTION
# -----------------------------

VOICE = "en-US-AndrewNeural"
# Alternative:
# en-GB-RyanNeural


async def async_speak(text):

    communicate = edge_tts.Communicate(
        text,
        VOICE
    )

    await communicate.save("jarvis_voice.mp3")


def speak(text):

    print(f"\nJarvis: {text}\n")

    asyncio.run(async_speak(text))

    pygame.mixer.init()

    pygame.mixer.music.load("jarvis_voice.mp3")

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.music.unload()

    os.remove("jarvis_voice.mp3")

    # Small pause before listening again
    time.sleep(0.4)


# -----------------------------
# SPEECH RECOGNITION
# -----------------------------

recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:

        print("\nListening...\n")

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:

            return ""

    try:

        text = recognizer.recognize_google(audio)

        print(f"You: {text}")

        return text.lower()

    except:

        return ""
# -----------------------------
# WAKE WORD SYSTEM
# -----------------------------

def wait_for_wake_word():

    wake_words = [
        "jarvis",
        "hey jarvis"
    ]

    while True:

        text = listen()

        if not text:
            continue

        # Global exit
        if "exit" in text:

            speak("Shutting down.")

            exit()

        if any(
            wake_word in text
            for wake_word in wake_words
        ):

            speak("Yes sir?")

            command = listen()

            return command