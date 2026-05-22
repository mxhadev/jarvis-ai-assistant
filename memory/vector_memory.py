import chromadb
from memory.embeddings import create_embedding

client = chromadb.PersistentClient(path="./memory_db")

collection = client.get_or_create_collection(
    name="jarvis_memory"
)

def store_memory(text, memory_id, category):
    embedding = create_embedding(text)

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[memory_id],
        metadatas=[{
            "category": category
        }]
    )
    embedding = create_embedding(text)

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[memory_id]
    )

def retrieve_memories(query, category=None, n_results=3):

    query_embedding = create_embedding(query)

    query_filter = None

    if category:
        query_filter = {
            "category": category
        }

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=query_filter
    )

    return results["documents"][0]

    return results["documents"][0]
def delete_memory(memory_text):

    results = collection.query(
        query_texts=[memory_text],
        n_results=1
    )

    if not results["ids"][0]:
        return False

    memory_id = results["ids"][0][0]

    collection.delete(ids=[memory_id])

    return True