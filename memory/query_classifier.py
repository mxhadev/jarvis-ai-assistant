import requests

VALID_CATEGORIES = [
    "identity",
    "preference",
    "goal",
    "project",
    "relationship",
    "habit",
    "experience",
    "skill",
    "other"
]

def classify_query(query):

    prompt = f"""
You are a query classification system.

Determine which memory category is MOST relevant to the user's question.

Valid categories:
identity
preference
goal
project
relationship
habit
experience
skill
other

Only reply with ONE category.

Examples:

"What are my goals?"
→ goal

"What do I like?"
→ preference

"What is my father's name?"
→ relationship

"What skills do I have?"
→ skill

User query:
{query}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    category = response.json()["response"].strip().lower()

    if category not in VALID_CATEGORIES:
        category = "other"

    return category