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

User:
type hello world

Output:
[
    {{
        "action": "type_text",
        "text": "hello world"
    }}
]

User:
press enter

Output:
[
    {{
        "action": "press_key",
        "key": "enter"
    }}
]

User:
take a screenshot

Output:
[
    {{
        "action": "take_screenshot"
    }}
]

User:
what's on my screen

Output:
[
    {{
        "action": "analyze_screen"
    }}
]

User:
read my screen

Output:
[
    {{
        "action": "analyze_screen"
    }}
]

User:
what is on my screen

Output:
[
    {{
        "action": "analyze_screen"
    }}
]

User:
click youtube

Output:
[
    {{
        "action": "click_text",
        "target": "youtube"
    }}
]

User:
click watch movie

Output:
[
    {{
        "action": "click_text",
        "target": "watch movie"
    }}
]

User:
press youtube

Output:
[
    {{
        "action": "click_text",
        "target": "watch movie"
    }}
]

User:
press watch movie

Output:
[
    {{
        "action": "click_text",
        "target": "watch movie"
    }}
]

User:
scroll down

Output:
[
    {{
        "action": "scroll_down"
    }}
]

User:
scroll up

Output:
[
    {{
        "action": "scroll_up"
    }}
]

User:
open youtube and search phonk music

Output:
[
    {{
        "action": "open_website",
        "target": "https://youtube.com"
    }},
    {{
        "action": "click_text",
        "target": "Search"
    }},
    {{
        "action": "type_text",
        "text": "phonk music"
    }},
    {{
        "action": "press_key",
        "key": "enter"
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