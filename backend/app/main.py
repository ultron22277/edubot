from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add root to path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from backend.app.services.rag_pipeline import (
    load_data,
    load_embedder,
    setup_vectorstore,
    index_data,
    get_answer,
)
from backend.app.services.chat_service import load_classifier, chat

app = FastAPI(title="EduBot API", version="1.0.0")

# ── CORS — allows frontend to talk to backend ─────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# ── Global variables ──────────────────────────────────────────────────────────
classifier = None
collection = None
embedder = None


# ── Load everything on startup ────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    global classifier, collection, embedder
    print("Loading classifier...")
    classifier = load_classifier()
    print("✅ Classifier loaded!")

    print("Loading embedder...")
    embedder = load_embedder()

    print("Setting up vector store...")
    data = load_data()
    collection = setup_vectorstore()
    index_data(collection, embedder, data)
    print("✅ Everything loaded!")


# ── Request model ─────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    question: str


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "EduBot is running!", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    response = chat(request.question, classifier, collection, embedder)
    return response
