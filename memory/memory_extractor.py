import requests
import json

VALID_CATEGORIES = [
    "identity",
    "preference",
    "goal",
    "project",
    "relationship",
    "habit",
    "experience",
    "skill",
    "ownership",
    "other"
]

CATEGORY_SYNONYMS = {

    "family_relation": "relationship",
    "friendship": "relationship",
    "romantic_relationship": "relationship",

    "career_goal": "goal",
    "life_goal": "goal",
    "future_ambition": "goal",

    "personal_preference": "preference",
    "favorite": "preference",

    "work_project": "project",
    "personal_project": "project",

    "daily_habit": "habit",

    "technical_skill": "skill"
}


def extract_memories(text):

    prompt = f"""
You are a memory extraction system for an AI assistant.

Extract important long-term memories from the user's message.

For each memory:
- extract ONLY explicit long-term user facts
- separate complete atomic facts
- do NOT extract sentence fragments
- do NOT extract vague phrases
- do NOT infer information
- do NOT create memories from questions
- do NOT create memories from assistant responses
- each memory must be meaningful standalone information
- assign ONE category

Valid categories:
identity
preference
goal
project
relationship
habit
experience
skill

Return ONLY valid JSON.

Format:
[
  {{
    "memory": "...",
    "category": "..."
  }}
]

Examples:

User:
"My name is Mahadev and I love motorcycles"

Output:
[
  {{
    "memory": "My name is Mahadev",
    "category": "identity"
  }},
  {{
    "memory": "I love motorcycles",
    "category": "preference"
  }}
]

User:
"My father's name is Pradeep and my mother is Sreeja"

Output:
[
  {{
    "memory": "My father's name is Pradeep",
    "category": "relationship"
  }},
  {{
    "memory": "My mother's name is Sreeja",
    "category": "relationship"
  }}
]

User message:
{text}
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
        memories = json.loads(result)

        for item in memories:

            category = item["category"]

            # Normalize synonym categories
            if category in CATEGORY_SYNONYMS:
                category = CATEGORY_SYNONYMS[category]

            # Validate final category
            if category not in VALID_CATEGORIES:
                category = "other"

            item["category"] = category

        return memories

    except:
        return []