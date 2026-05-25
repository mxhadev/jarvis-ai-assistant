import speech_recognition as sr
import edge_tts
import asyncio
import pygame
import uuid
import time
# -----------------------------------
# SPEECH RECOGNIZER
# -----------------------------------

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.pause_threshold = 0.8
recognizer.dynamic_energy_threshold = True

# -----------------------------------
# LISTEN
# -----------------------------------

def listen():

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            text = recognizer.recognize_google(
                audio
            )

            print(f"You: {text}")

            return text.lower()

        except sr.WaitTimeoutError:

            return ""

        except sr.UnknownValueError:

            return ""

        except sr.RequestError:

            return ""

# -----------------------------------
# WAKE WORD
# -----------------------------------

def wait_for_wake_word():

    while True:

        text = listen()

        if not text:
            continue

        if (
            "hey jarvis" in text
            or "jarvis" in text
        ):

            print("Jarvis: Yes sir?")

            speak("Yes sir")

            command = listen()

            return command

# -----------------------------------
# TTS
# -----------------------------------

async def async_speak(text):

    filename = f"voice_{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(
        text,
        voice="en-US-GuyNeural",
        rate="+20%"
    )

    await communicate.save(filename)

    return filename

# -----------------------------------
# SPEAK
# -----------------------------------

def speak(text):

    filename = asyncio.run(
        async_speak(text)
    )

    if not pygame.mixer.get_init():

        pygame.mixer.init()

    pygame.mixer.music.load(filename)

    pygame.mixer.music.play()

    clock = pygame.time.Clock()

    start_time = time.time()

    while pygame.mixer.music.get_busy():

         clock.tick(10)

        # FORCE EXIT IF APP IS CLOSING

         if time.time() - start_time > 10:
              break