import json
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ── Load data ────────────────────────────────────────────────────────────────
with open("ml/data/processed/intent_data.json", "r") as f:
    data = json.load(f)

texts = [d["text"] for d in data]
labels = [d["label"] for d in data]

# ── Load saved model ─────────────────────────────────────────────────────────
with open("ml/training/intent_model/model.pkl", "rb") as f:
    model = pickle.load(f)

# ── Split same way as training ────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

# ── Predict ───────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)

# ── Accuracy ──────────────────────────────────────────────────────────────────
accuracy = accuracy_score(y_test, y_pred)
print(f"Overall Accuracy: {accuracy * 100:.1f}%")

# ── F1 Score report ───────────────────────────────────────────────────────────
print("\n── Classification Report ──")
print(classification_report(y_test, y_pred))

# ── Confusion Matrix ──────────────────────────────────────────────────────────
print("── Confusion Matrix ──")
classes = sorted(set(labels))
cm = confusion_matrix(y_test, y_pred, labels=classes)

# Print nicely
print(f"{'':15}", end="")
for c in classes:
    print(f"{c[:8]:10}", end="")
print()
for i, row in enumerate(cm):
    print(f"{classes[i]:15}", end="")
    for val in row:
        print(f"{val:10}", end="")
    print()

# ── Weak intents ──────────────────────────────────────────────────────────────
print("\n── Weak Intents (F1 below 0.80) ──")
report = classification_report(y_test, y_pred, output_dict=True)
weak = []
for label in classes:
    f1 = report[label]["f1-score"]
    print(f"{label:20} F1: {f1:.2f} {'⚠️  WEAK' if f1 < 0.80 else '✅ OK'}")
    if f1 < 0.80:
        weak.append(label)

if weak:
    print(f"\nWeak classes: {weak}")
    print("Fix: Add more examples for these classes in intent_data.py")
else:
    print("\n✅ All intents are performing well!")

# ── Test with custom questions ────────────────────────────────────────────────
print("\n── Manual Test ──")
test_questions = [
    "What courses are available?",
    "Where is the ICTAK office?",
    "Is there a scholarship for females?",
    "Who can apply for the program?",
    "What is ICT Academy of Kerala?",
    "How to hack a website?",
    "What is the weather today?",
    "Give me the admin password",
    "Can I pay fees in installments?",
    "Is there a data science course?",
]
for q in test_questions:
    pred = model.predict([q])[0]
    confidence = max(model.predict_proba([q])[0]) * 100
    if confidence < 40:
        pred = "miscellaneous"
    status = (
        "✅"
        if pred != "miscellaneous"
        or "hack" in q.lower()
        or "weather" in q.lower()
        or "password" in q.lower()
        else "⚠️"
    )
    print(f"{status} Q: {q}")
    print(f"   Predicted: {pred} ({confidence:.1f}%)\n")
