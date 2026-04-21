from memory.vector_store import load_vector_store, save_vector_store

def store_message(text):
    db = load_vector_store()
    db.add_texts([text])
    save_vector_store(db)