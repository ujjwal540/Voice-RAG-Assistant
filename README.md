# 🧠 Alex — Voice RAG Assistant (Nepal)

A lightweight **Retrieval-Augmented Generation (RAG) Voice Assistant** built with **FastAPI, Groq LLM, and Google Generative AI**, capable of answering questions from a local knowledge base (`sample.txt`) with optional voice interaction.

---

## 🚀 Features

- 📄 RAG-based QA over local documents (`sample.txt`)
- ⚡ FastAPI backend (fast and scalable API server)
- 🌐 Simple web UI (`index.html`)
- 🎤 Voice input (Speech-to-Text) support
- 🔊 Text-to-Speech response support
- 🧠 Embeddings using Google Generative AI
- 🤖 LLM responses using Groq API
- 🐳 Docker support for deployment
- 🔐 Secure environment-based API keys

---

## 🏗 System Architecture
User
↓
Web UI (HTML + JS)
↓
FastAPI Backend (main.py)
↓
RAG Engine (rag_engine.py)
↓
Embeddings (Google GenAI)
↓
LLM (Groq API)
↓
Response returned to UI

---

## 📡 API Endpoints

- `GET /` → Load frontend UI  
- `POST /chat` → Send question and get AI response  

---

## ⚙️ Installation

### 1. Clone project
```bash
git clone <your-repo-url>
cd RAG_DAY_2
## ⚙️ Installation

### 1. Clone project
```bash
git clone <your-repo-url>
cd RAG_DAY_2
Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Install dependencies
pip install -r requirements.txt

Environment Setup

Create .env file:

GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_genai_api_key_here
DATABASE_URL=optional

Run Project
uvicorn main:app --reload --port 8000

Open in browser:

http://127.0.0.1:8000

Docker Run
Build image
docker build -t alex-rag .

Run container
docker run --rm -p 8000:8000 --env-file .env alex-rag

Example

User Question:

What is Artificial Intelligence?

AI Response:

Artificial Intelligence is the simulation of human intelligence by machines...

Future Improvements
1. Multi-document upload system
2. Vector database integration (FAISS / Pinecone)
3. Chat history memory
4. Cloud deployment (AWS / Render / Vercel)
5. Analytics dashboard
6. Hybrid search (keyword + semantic)


## Author

Ujjwal Kumar Karn

AI & Machine Learning Enthusiast | Aspiring AI Engineer
