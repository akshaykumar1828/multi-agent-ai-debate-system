import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from data.personas import personas

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

DB_PATH = "faiss_index"

if os.path.exists(DB_PATH):
    vectorstore = FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)
else:
    documents = [
        Document(page_content=p["description"], metadata={"bot": p["bot"]})
        for p in personas
    ]

    vectorstore = FAISS.from_documents(documents, embedding_model)
    vectorstore.save_local(DB_PATH)


def route_post_to_bots(post, k=2):
    results = vectorstore.similarity_search(post, k=k)
    return [doc.metadata["bot"] for doc in results]