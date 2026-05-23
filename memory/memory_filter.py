import requests

def should_store_memory(text):

    text_lower = text.lower()

    # Fast question detection
    question_starters = [
        "what",
        "whats",
        "who",
        "where",
        "when",
        "why",
        "how",
        "do",
        "does",
        "did",
        "can",
        "could",
        "would",
        "is",
        "are"
    ]

    words = text_lower.split()

    if "?" in text or (words and words[0] in question_starters):
        return False

    prompt = f"""
You are a memory evaluation system for an AI assistant.

Your task is to decide whether the user's message contains important long-term information worth remembering.

IMPORTANT memories include:
- identity
- personal preferences
- goals
- habits
- relationships
- ownership
- long-term projects
- important experiences
- skills

DO NOT store:
- questions
- greetings
- casual chat
- temporary discussions
- assistant instructions
- vague statements
- jokes
- short reactions

Only reply with:
YES
or
NO

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

    result = response.json()["response"].strip().upper()

    return "YES" in result