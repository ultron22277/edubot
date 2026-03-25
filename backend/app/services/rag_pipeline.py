import json
import os
import chromadb
from sentence_transformers import SentenceTransformer


# ── Load ICTAK data ───────────────────────────────────────────────────────────
def load_data():
    with open("ml/data/processed/ictak_cleaned.json", "r", encoding="utf-8") as f:
        return json.load(f)


# ── Setup ChromaDB ────────────────────────────────────────────────────────────
def setup_vectorstore():
    client = chromadb.PersistentClient(path="ml/data/vectorstore")
    collection = client.get_or_create_collection(name="ictak_knowledge")
    return collection


# ── Load embedding model ──────────────────────────────────────────────────────
def load_embedder():
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Embedding model loaded!")
    return model


# ── Index all ICTAK data ──────────────────────────────────────────────────────
def index_data(collection, embedder, data):
    existing = collection.count()
    if existing > 0:
        print(f"✅ Vector store already has {existing} entries, skipping indexing")
        return

    print(f"Indexing {len(data)} Q&A pairs...")
    for i, item in enumerate(data):
        text = f"Q: {item['question']} A: {item['answer']}"
        embedding = embedder.encode(text).tolist()
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{"question": item["question"], "answer": item["answer"]}],
        )
    print(f"✅ Indexed {len(data)} entries!")


# ── Search for relevant answer ────────────────────────────────────────────────
def search(query, collection, embedder, top_k=3):
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["metadatas"][0]


# ── Generate answer ───────────────────────────────────────────────────────────
def get_answer(query, collection, embedder):
    results = search(query, collection, embedder)
    if not results:
        return "Sorry, I could not find an answer to your question."

    # Return the best matching answer
    best_match = results[0]
    return best_match["answer"]


# ── Main (test the pipeline) ──────────────────────────────────────────────────
if __name__ == "__main__":
    data = load_data()
    embedder = load_embedder()
    collection = setup_vectorstore()
    index_data(collection, embedder, data)

    print("\n--- Testing RAG Pipeline ---\n")
    test_questions = [
        "What is the age limit for applying?",
        "Where is the ICTAK office?",
        "Is there a scholarship for female candidates?",
        "What courses does ICTAK offer?",
        "What is ICT Academy of Kerala?",
        "How long is the course?",
    ]

    for q in test_questions:
        answer = get_answer(q, collection, embedder)
        print(f"Q: {q}")
        print(f"A: {answer}")
        print()

    print("🎉 RAG Pipeline working!")
