from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# DB path
DB_PATH = "memory/faiss_index"

# Load or create DB
def load_vector_store():
    if os.path.exists(DB_PATH):
        return FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        return FAISS.from_texts(["initial memory"], embeddings)

# Save DB
def save_vector_store(db):
    db.save_local(DB_PATH)