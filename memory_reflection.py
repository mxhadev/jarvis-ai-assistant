from memory.vector_memory import collection


IMPORTANT_CATEGORIES = [
    "identity",
    "goal",
    "relationship",
    "habit",
    "project"
]


def reflect_on_memories():

    results = collection.get(
        include=["documents", "metadatas"]
    )

    ids = results["ids"]
    documents = results["documents"]
    metadatas = results["metadatas"]

    removed_count = 0
    reinforced_count = 0

    for i in range(len(ids)):

        memory_id = ids[i]

        memory_text = documents[i]

        metadata = metadatas[i]

        importance = metadata.get(
            "importance",
            1
        )

        category = metadata.get(
            "category",
            "other"
        )

        # -----------------------------------
        # REMOVE WEAK MEMORIES
        # -----------------------------------

        if (
            importance <= 1
            and len(memory_text.split()) < 4
        ):

            collection.delete(
                ids=[memory_id]
            )

            removed_count += 1

            continue

        # -----------------------------------
        # REINFORCE IMPORTANT MEMORIES
        # -----------------------------------

        if category in IMPORTANT_CATEGORIES:

            importance += 1

            collection.update(
                ids=[memory_id],
                metadatas=[{
                    **metadata,
                    "importance": importance
                }]
            )

            reinforced_count += 1

    return (
        f"Reflection complete. "
        f"Removed {removed_count} weak memories. "
        f"Reinforced {reinforced_count} important memories."
    )