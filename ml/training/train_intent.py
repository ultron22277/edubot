import json
import pickle
import os
from collections import Counter
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ── Load data ────────────────────────────────────────────────────────────────
with open("ml/data/processed/intent_data.json", "r") as f:
    data = json.load(f)

texts = [d["text"] for d in data]
labels = [d["label"] for d in data]

print(f"Total examples: {len(texts)}")
print(f"Class distribution: {Counter(labels)}")

# ── Split ────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)
print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# ── Train ────────────────────────────────────────────────────────────────────
model = Pipeline(
    [
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", C=5)),
    ]
)

model.fit(X_train, y_train)

# ── Evaluate ─────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy: {accuracy * 100:.1f}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred))

# ── Save model ────────────────────────────────────────────────────────────────
os.makedirs("ml/training/intent_model", exist_ok=True)

with open("ml/training/intent_model/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("ml/training/intent_model/labels.json", "w") as f:
    json.dump(list(set(labels)), f)

print("✅ Model saved to ml/training/intent_model/")
print("🎉 Day 4 complete!")

# ── Quick test ────────────────────────────────────────────────────────────────
print("\n--- Quick Test ---")
test_questions = [
    "What courses are available?",
    "Where is the office?",
    "Is there a scholarship?",
    "Who can apply?",
    "What is ICTAK?",
    "How to hack a website?",
    "What is the weather today?",
    "Tell me a joke",
]
for q in test_questions:
    pred = model.predict([q])[0]
    confidence = max(model.predict_proba([q])[0]) * 100
    if confidence < 40:
        pred = "miscellaneous"
    print(f"Q: {q}")
    print(f"A: {pred} ({confidence:.1f}% confident)\n")
