import pickle
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from backend.app.services.rag_pipeline import get_answer


# ── Load intent classifier ────────────────────────────────────────────────────
def load_classifier():
    model_path = os.path.join(BASE_DIR, "ml", "training", "intent_model", "model.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model


# ── Classify intent ───────────────────────────────────────────────────────────
def classify_intent(question, classifier):
    pred = classifier.predict([question])[0]
    confidence = max(classifier.predict_proba([question])[0]) * 100
    if confidence < 40:
        pred = "miscellaneous"
    return pred, confidence


# ── Responses ─────────────────────────────────────────────────────────────────
MISC_RESPONSE = (
    "I can only answer questions about ICT Academy of Kerala. "
    "You can ask me about courses, admissions, fees, contact details, or about ICTAK."
)

LOW_CONFIDENCE_RESPONSE = (
    "I don't have enough information regarding this. "
    "Please contact ICTAK directly at info@ictkerala.org or call +91 75 940 51437."
)


# ── Main chat function ────────────────────────────────────────────────────────
def chat(question: str, classifier, collection, embedder) -> dict:
    # Clean the question — remove quotes and extra spaces
    question = question.strip().strip('"').strip("'").strip()

    # Step 1 — classify intent
    intent, confidence = classify_intent(question, classifier)

    # Step 2 — block miscellaneous
    if intent == "miscellaneous":
        return {
            "question": question,
            "answer": MISC_RESPONSE,
            "intent": "miscellaneous",
            "confidence": round(confidence, 1),
        }

    # Step 3 — low confidence check
    if confidence < 40:
        return {
            "question": question,
            "answer": LOW_CONFIDENCE_RESPONSE,
            "intent": "unknown",
            "confidence": round(confidence, 1),
        }

    # Step 4 — get answer from RAG
    answer = get_answer(question, collection, embedder)

    return {
        "question": question,
        "answer": answer,
        "intent": intent,
        "confidence": round(confidence, 1),
    }
