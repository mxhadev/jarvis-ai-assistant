import uuid

from memory.memory_extractor import extract_memories
from memory.query_classifier import classify_query

from memory.vector_memory import (
    store_memory,
    retrieve_memories,
    delete_memory
)


def save_memory(text):

    extracted_memories = extract_memories(text)

    for item in extracted_memories:

        memory_text = item["memory"].strip()

        # Skip weak memories
        if len(memory_text.split()) < 3:
            continue

        bad_phrases = [
            "in the future",
            "not provided",
            "unknown",
            "something",
            "this message"
        ]

        if any(
            phrase in memory_text.lower()
            for phrase in bad_phrases
        ):
            continue

        category = item["category"]

        memory_id = str(uuid.uuid4())

        try:

            store_memory(
                memory_text,
                memory_id,
                category
            )

        except:
            pass


def get_memories(query):

    try:

        category = classify_query(query)

        return retrieve_memories(
            query,
            category=category
        )

    except:
        return []


def forget_memory(text):

    success = delete_memory(text)

    if success:
        return "Memory deleted successfully."

    return "Could not find matching memory."