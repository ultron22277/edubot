# EduBot 🎓
AI-Powered Query Chatbot for ICT Academy of Kerala

## About
EduBot is an intelligent chatbot that answers queries about ICT Academy of Kerala (ICTAK) instantly. It uses Natural Language Processing to understand questions and provide accurate answers about courses, admissions, fees, contact details, and more.

## Features
- 🤖 AI-powered intent classification (89%+ accuracy)
- 🔍 RAG pipeline for accurate answers
- 🛡️ Blocks irrelevant/harmful questions
- 💬 Beautiful chat UI with typing animation
- 📱 Mobile friendly
- ⚡ Real-time responses
- 🌐 Built on ICTAK website data

## Tech Stack
- **Backend:** FastAPI (Python)
- **NLP:** Scikit-learn Intent Classifier + LangChain RAG
- **Vector Store:** ChromaDB
- **Embeddings:** Sentence Transformers
- **Frontend:** React.js + Vite
- **Deploy:** Docker

## Project Structure
```
edubot/
  backend/          # FastAPI app, RAG pipeline, intent classifier
  frontend/         # React chat interface
  ml/               # Training data, models, datasets
  docs/             # Documentation
```

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173

## Author
Achal Dev