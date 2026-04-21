from memory.vector_store import load_vector_store

def retrieve_memory(query, k=3):
    db = load_vector_store()
    docs = db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in docs])