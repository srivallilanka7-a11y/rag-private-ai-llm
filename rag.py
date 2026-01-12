from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from db import collection
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def store_pdf_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    collection.delete_many({})  # Clear old data

    for chunk in chunks:
        vector = embedding_model.embed_query(chunk)
        collection.insert_one({
            "text": chunk,
            "embedding": vector
        })

def retrieve_context(query):
    query_vector = embedding_model.embed_query(query)

    docs = collection.find()
    scored = []

    for doc in docs:
        score = sum(a*b for a,b in zip(query_vector, doc["embedding"]))
        scored.append((score, doc["text"]))

    scored.sort(reverse=True)
    return " ".join([text for _, text in scored[:3]])