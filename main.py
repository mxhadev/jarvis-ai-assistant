import requests
import time
import threading
from habit_tracker import track_action
from web_search import search_web
from voice import (
    wait_for_wake_word,
    speak
)

from actions.action_filter import (
    is_action_request
)

from memory.memory_filter import should_store_memory

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

conversation_history = []

MAX_HISTORY = 6

print("Jarvis is online.")
print("Say 'Hey Jarvis' to activate.\n")

while True:

    user_input = wait_for_wake_word()

    if not user_input:
        continue

    if "exit" in user_input:

        speak("Shutting down.")

        break

    # -----------------------------------
    # SMART ACKNOWLEDGEMENT SYSTEM
    # -----------------------------------

    response_ready = False

    def delayed_acknowledgement():

        time.sleep(2)

        if not response_ready:
            speak("One moment sir.")

    threading.Thread(
        target=delayed_acknowledgement,
        daemon=True
    ).start()

    # -----------------------------------
    # ACTION FILTER
    # -----------------------------------

    if is_action_request(user_input):

        action_list = route_action(user_input)

        # Check if any real action exists
        real_actions = [
            action
            for action in action_list
            if action["action"] != "none"
        ]

        if real_actions:

            response_ready = True

            for action_data in real_actions:

                action_name = action_data["action"]

                # Small delay between actions
                time.sleep(1)

                result = execute_action(action_data)
                track_action(action_name)
                # Stop workflow if action failed
                if "could not" in result.lower():
    
                     speak(result)

                     break

                print(f"\nJarvis: {result}\n")

                speak(result)

                # Extra wait after browser/app actions
                if action_name in [
                    "open_website",
                    "google_search",
                    "youtube_search"
                ]:
                    time.sleep(3)

                # Clear short-term memory if forgetting
                if action_name == "forget_memory":
                    conversation_history = []

            continue

    # -----------------------------------
    # MEMORY RETRIEVAL
    # -----------------------------------

    memories = get_memories(user_input)

    memory_text = "\n".join(memories)
    # -----------------------------------
    # WEB SEARCH DETECTION
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

        print("Jarvis is searching the web...")
        web_info = search_web(user_input)
    # -----------------------------------
    # PROMPT BUILDING
    # -----------------------------------

    prompt = f"""
You are Jarvis, a smart and personal AI assistant.

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

    speak(jarvis_response)

    # -----------------------------------
    # UPDATE CONVERSATION HISTORY
    # -----------------------------------

    conversation_history.append(
        f"User: {user_input}"
    )

    conversation_history.append(
        f"Jarvis: {jarvis_response}"
    )

    # Keep only recent exchanges
    conversation_history = conversation_history[-MAX_HISTORY:]

    # -----------------------------------
    # MEMORY STORAGE
    # -----------------------------------

    if should_store_memory(user_input):
        save_memory(user_input)