import requests
import json

from actions.tool_registry import TOOLS


def route_action(user_input):

    tool_text = ""

    for tool in TOOLS:

        tool_text += f"""
Tool Name:
{tool['name']}

Description:
{tool['description']}

Arguments:
{tool['arguments']}
"""

    prompt = f"""
You are an AI action routing system.

Your task is to determine which tools should be used based on the user's request.

Available tools:
{tool_text}

RULES:
- Return ONLY valid JSON
- Never explain
- Never add markdown
- Multiple actions are allowed
- Extract arguments carefully
- Use the most suitable tools
- NEVER use forget_memory unless the user EXPLICITLY asks to forget/delete/remove memory
- Questions are NOT actions
- Information retrieval questions should NOT trigger actions
- ONLY trigger tools when the user clearly wants an action executed

Examples:

User:
open youtube

Output:
[
    {{
        "action": "open_website",
        "target": "https://youtube.com"
    }}
]

User:
search google for python tutorials

Output:
[
    {{
        "action": "google_search",
        "query": "python tutorials"
    }}
]

User:
play interstellar theme

Output:
[
    {{
        "action": "play_youtube",
        "query": "interstellar theme"
    }}
]
User:
forget my father's name

Output:
[
    {{
        "action": "forget_memory",
        "query": "father's name"
    }}
]
User:
open youtube and play phonk music

Output:
[
    {{
        "action": "open_website",
        "target": "https://youtube.com"
    }},
    {{
        "action": "play_youtube",
        "query": "phonk music"
    }}
]

User:
search youtube for startup podcasts and open vscode

Output:
[
    {{
        "action": "youtube_search",
        "query": "startup podcasts"
    }},
    {{
        "action": "open_vscode"
    }}
]

If no action is needed:
[
    {{
        "action": "none"
    }}
]

User request:
{user_input}
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

    try:

        parsed = json.loads(result)

        # Convert single action into list
        if isinstance(parsed, dict):
            parsed = [parsed]

        return parsed

    except:

        print("\n[Action Router Error]\n")

        return [
            {
                "action": "none"
            }
        ]