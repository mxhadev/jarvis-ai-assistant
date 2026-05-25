import requests
import time
import threading
import sys
import os
import random
from PyQt6.QtWidgets import QApplication

from jarvis_hud import JarvisHUD

from habit_tracker import track_action

from web_search import search_web

from voice import (
    wait_for_wake_word,
    speak
)

from actions.action_filter import (
    is_action_request
)

from memory.memory_filter import (
    should_store_memory
)

from memory.memory_manager import (
    save_memory,
    get_memories
)

from actions.action_router import (
    route_action
)

from actions.tool_executor import (
    execute_action
)
ACKNOWLEDGEMENTS = [
    "Yes sir?",
    "I'm listening sir.",
    "Go ahead sir.",
    "Ready when you are sir.",
    "At your service sir.",
    "What can I do for you sir?"
]

THANK_RESPONSES = [
    "Always sir.",
    "Happy to help.",
    "Anytime sir.",
    "That's what I'm here for.",
    "Glad to assist."
]

HOW_ARE_YOU_RESPONSES = [
    "Running smoothly sir.",
    "All systems operational.",
    "Doing great sir.",
    "Better now that you're here.",
    "Functioning at peak efficiency."
]

FUNNY_RESPONSES = [
    "I would smile if I had a face.",
    "Still less buggy than most apps.",
    "I try my best sir.",
    "Surviving another day in Python."
]

# -----------------------------------
# HUD STARTUP
# -----------------------------------

app = QApplication(sys.argv)

hud = JarvisHUD()

hud.show()


def update_hud():

    app.processEvents()


# -----------------------------------
# MEMORY
# -----------------------------------

conversation_history = []

MAX_HISTORY = 6

print("Jarvis is online.")

print("Say 'Hey Jarvis' to activate.\n")


# -----------------------------------
# ANIMATED SUBTITLE
# -----------------------------------

def animated_subtitle(text):

    displayed_text = ""

    words = text.split()

    for word in words:

        displayed_text += word + " "

        if len(displayed_text) > 180:

            displayed_text = (
                "..."
                + displayed_text[-180:]
            )

        hud.set_subtitle(
            displayed_text
        )

        update_hud()

        time.sleep(0.03)


# -----------------------------------
# SAFE SPEAK THREAD
# -----------------------------------

def threaded_speak(text):

    speak_thread = threading.Thread(
        target=speak,
        args=(text,),
        daemon=True
    )

    speak_thread.start()

    return speak_thread


# -----------------------------------
# FORCE CLOSE APP
# -----------------------------------

def force_shutdown():

    os._exit(0)
# -----------------------------------
# JARVIS LOOP
# -----------------------------------

def jarvis_loop():

    global conversation_history

    while True:

        # -----------------------------------
        # LISTENING
        # -----------------------------------

        hud.set_mode("LISTENING")

        hud.voice_status = "Listening"

        hud.set_subtitle(
            "Listening..."
        )

        hud.set_audio_level(15)

        update_hud()

        user_input = wait_for_wake_word()

        hud.set_audio_level(0)

        update_hud()

        if not user_input:
            continue

        hud.set_subtitle(
            f"You: {user_input}"
        )

        update_hud()

        # -----------------------------------
        # EXIT
        # -----------------------------------

        if (
            "exit" in user_input.lower()
            or "shutdown" in user_input.lower()
            or "close jarvis" in user_input.lower()
        ):

            hud.set_mode("SHUTDOWN")

            hud.voice_status = "Shutdown"

            hud.set_subtitle(
                "Shutting down..."
            )

            hud.set_audio_level(10)

            update_hud()

            print("Shutting down...")
            time.sleep(0.3)

            force_shutdown()

            return

        # -----------------------------------
        # SMART ACKNOWLEDGEMENT
        # -----------------------------------

        response_ready = False

        def delayed_acknowledgement():

            time.sleep(2)

            if not response_ready:

                hud.set_mode("WAITING")

                hud.voice_status = "Waiting"

                hud.set_subtitle(
                    "One moment sir..."
                )

                hud.set_audio_level(25)

                update_hud()

                threaded_speak(
                    "One moment sir."
                )

        threading.Thread(
            target=delayed_acknowledgement,
            daemon=True
        ).start()

        # -----------------------------------
        # ACTION SYSTEM
        # -----------------------------------

        if is_action_request(user_input):

            action_list = route_action(user_input)

            real_actions = [
                action
                for action in action_list
                if action["action"] != "none"
            ]

            if real_actions:

                response_ready = True

                for action_data in real_actions:

                    action_name = action_data["action"]

                    hud.set_mode("EXECUTING")

                    hud.voice_status = "Executing"

                    hud.set_subtitle(
                        f"Executing: {action_name}"
                    )

                    hud.set_audio_level(20)

                    update_hud()

                    time.sleep(0.5)

                    result = execute_action(
                        action_data
                    )

                    track_action(action_name)

                    # FAILURE

                    if "could not" in result.lower():

                        hud.set_mode("ERROR")

                        hud.voice_status = "Error"

                        hud.set_subtitle(
                            result
                        )

                        hud.set_audio_level(35)

                        update_hud()

                        threaded_speak(result)

                        break

                    print(f"\nJarvis: {result}\n")

                    hud.set_mode("SPEAKING")

                    hud.voice_status = "Speaking"

                    hud.set_audio_level(35)

                    animated_subtitle(
                        f"Jarvis: {result}"
                    )

                    update_hud()

                    threaded_speak(result)

                    # PAGE LOAD WAIT

                    if action_name in [
                        "open_website",
                        "google_search",
                        "youtube_search"
                    ]:

                        hud.set_mode("LOADING")

                        hud.voice_status = "Loading"

                        hud.set_subtitle(
                            "Waiting for page..."
                        )

                        update_hud()

                        time.sleep(2)

                    if action_name == "forget_memory":

                        conversation_history = []

                hud.set_audio_level(0)

                update_hud()

                continue

        # -----------------------------------
        # MEMORY RETRIEVAL
        # -----------------------------------

        memories = get_memories(
            user_input
        )

        memory_text = "\n".join(memories)

        # -----------------------------------
        # WEB SEARCH
        # -----------------------------------

        web_info = ""

        web_keywords = [
            "latest",
            "news",
            "today",
            "current",
            "weather",
            "update",
            "recent",
            "who won",
            "price",
            "release"
        ]

        if any(
            keyword in user_input.lower()
            for keyword in web_keywords
        ):

            hud.set_mode("WEB SEARCH")

            hud.voice_status = "Searching"

            hud.set_subtitle(
                "Searching the web..."
            )

            hud.set_audio_level(20)

            update_hud()

            web_info = search_web(
                user_input
            )

        # -----------------------------------
        # THINKING
        # -----------------------------------

        hud.set_mode("THINKING")

        hud.voice_status = "Thinking"

        hud.set_subtitle(
            "Thinking..."
        )

        hud.set_audio_level(30)

        update_hud()

        # -----------------------------------
        # PROMPT
        # -----------------------------------

        prompt = f"""
You are Jarvis, a smart and futuristic personal AI assistant.

Relevant memories:
{memory_text}

Live web information:
{web_info}

Conversation history:
{chr(10).join(conversation_history)}

User: {user_input}

Jarvis:
"""

        # -----------------------------------
        # AI RESPONSE
        # -----------------------------------

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        jarvis_response = data["response"]

        response_ready = True

        # -----------------------------------
        # RESPONSE DISPLAY
        # -----------------------------------

        hud.set_mode("SPEAKING")

        hud.voice_status = "Speaking"

        hud.set_audio_level(45)

        animated_subtitle(
            f"Jarvis: {jarvis_response}"
        )

        update_hud()

        threaded_speak(
            jarvis_response
        )

        hud.set_audio_level(0)

        hud.set_mode("ONLINE")

        hud.voice_status = "Online"

        update_hud()

        # -----------------------------------
        # CONVERSATION MEMORY
        # -----------------------------------

        conversation_history.append(
            f"User: {user_input}"
        )

        conversation_history.append(
            f"Jarvis: {jarvis_response}"
        )

        conversation_history = (
            conversation_history[-MAX_HISTORY:]
        )

        # -----------------------------------
        # MEMORY STORAGE
        # -----------------------------------

        if should_store_memory(user_input):

            save_memory(user_input)


# -----------------------------------
# START BACKEND THREAD
# -----------------------------------

jarvis_thread = threading.Thread(
    target=jarvis_loop,
    daemon=True
)

jarvis_thread.start()

# -----------------------------------
# QT EVENT LOOP
# -----------------------------------

sys.exit(app.exec())