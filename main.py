import requests

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
import actions.tools

print(actions.tools.__file__)

conversation_history = ""

print("Jarvis is online.")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Jarvis shutting down.")
        break

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

            for action_data in real_actions:

                result = execute_action(action_data)
                print(f"\nJarvis: {result}\n")

                # Clear short-term memory if forgetting
                if action_data["action"] == "forget_memory":
                    conversation_history = ""

            continue

    # -----------------------------------
    # MEMORY RETRIEVAL
    # -----------------------------------

    memories = get_memories(user_input)

    memory_text = "\n".join(memories)

    # -----------------------------------
    # PROMPT BUILDING
    # -----------------------------------

    prompt = f"""
You are Jarvis, a smart and personal AI assistant.

Relevant memories:
{memory_text}

Conversation history:
{conversation_history}

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

    print("\nJarvis:", jarvis_response)
    print()

    # -----------------------------------
    # UPDATE CONVERSATION HISTORY
    # -----------------------------------

    conversation_history += f"\nUser: {user_input}"
    conversation_history += f"\nJarvis: {jarvis_response}"

    # -----------------------------------
    # MEMORY STORAGE
    # -----------------------------------

    if should_store_memory(user_input):
        save_memory(user_input)