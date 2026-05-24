from memory.vector_memory import collection


IMPORTANT_CATEGORIES = [
    "identity",
    "goal",
    "relationship",
    "habit",
    "project"
]


def reinforce_memory(memory_text):

    results = collection.query(
        query_texts=[memory_text],
        n_results=1
    )

    if not results["ids"][0]:
        return

    memory_id = results["ids"][0][0]

    metadata = results["metadatas"][0][0]

    importance = metadata.get(
        "importance",
        1
    )

    importance += 1

    collection.update(
        ids=[memory_id],
        metadatas=[{
            **metadata,
            "importance": importance
        }]
    )