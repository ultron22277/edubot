import json
import re

# ── Load raw data ────────────────────────────────────────────────────────────
with open("ml/data/raw/ictak_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

print(f"Loaded {len(raw_data)} raw Q&A pairs")


# ── Clean function ───────────────────────────────────────────────────────────
def clean_text(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)  # remove extra spaces
    text = re.sub(r"[^\w\s.,?!@+()/-]", "", text)  # remove weird characters
    return text


# ── Clean all pairs ──────────────────────────────────────────────────────────
cleaned = []
for item in raw_data:
    q = clean_text(item["question"])
    a = clean_text(item["answer"])
    if q and a:  # only keep if both are non-empty
        cleaned.append({"question": q, "answer": a})

print(f"Cleaned {len(cleaned)} Q&A pairs")

# ── Save cleaned data ────────────────────────────────────────────────────────
with open("ml/data/processed/ictak_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2, ensure_ascii=False)

print("✅ Saved to ml/data/processed/ictak_cleaned.json")

# ── Preview first 3 entries ──────────────────────────────────────────────────
print("\n--- Preview ---")
for item in cleaned[:3]:
    print(f"Q: {item['question']}")
    print(f"A: {item['answer']}")
    print()

print("🎉 Day 2 data cleaning complete!")
