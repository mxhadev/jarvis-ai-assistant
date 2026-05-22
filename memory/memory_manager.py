from memory.memory_extractor import extract_memories
from memory.query_classifier import classify_query
from memory.vector_memory import delete_memory
from memory.vector_memory import (
    store_memory,
    retrieve_memories
)

memory_counter = 0

def save_memory(text):
    global memory_counter

    extracted_memories = extract_memories(text)

    print(f"\n[Extracted Memories] {extracted_memories}\n")

    for item in extracted_memories:

        memory_text = item["memory"]
        # Skip weak or useless memories
        if len(memory_text.split()) < 3:
            continue

        bad_phrases = [
             "in the future",
             "not provided",
             "unknown",
             "something",
             "this message"
        ]

        if any(phrase in memory_text.lower() for phrase in bad_phrases):
            continue
        category = item["category"]

        memory_id = f"memory_{memory_counter}"

        store_memory(
            memory_text,
            memory_id,
            category
        )

        memory_counter += 1

def get_memories(query):

    category = classify_query(query)

    print(f"\n[Query Category] {category}\n")

    return retrieve_memories(
        query,
        category=category
    )
def forget_memory(text):

    success = delete_memory(text)

    if success:
        return "Memory deleted successfully."

    return "Could not find matching memory."