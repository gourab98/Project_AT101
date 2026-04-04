# 📖 Project_AT101 — Bengali Scripture AI Platform

An AI-powered question-answering platform built on the writings of **Sri Sri Thakur Anukulchandra**. Devotees can ask questions in Bengali or English and receive answers grounded entirely in the guru's own words — with source book references for every response.

Built using **Retrieval-Augmented Generation (RAG)**: the system searches 125+ scanned Bengali books, retrieves the most relevant passages, and generates answers using a local open-source LLM — no API key or cloud cost required.

---

## ✨ Features

- 🔍 Semantic search across 125+ Bengali scripture books
- 🤖 Answers generated entirely from the guru's actual writings
- 📚 Every answer includes source book references
- 🌐 Supports questions in both Bengali and English
- 🔒 Fully local — no data sent to external servers
- 💬 Clean chat interface for devotees

---

## 🏗️ Architecture

```
User Question
     │
     ▼
[React Frontend]  ──POST /ask──▶  [FastAPI Backend]
                                        │
                          ┌─────────────┼─────────────┐
                          ▼             ▼             ▼
                    Embed question   Qdrant DB     Ollama LLM
                    (LaBSE model)   (vector search) (Llama 3.1)
                          │             │
                          └──── Top 5 relevant passages ────▶ Generate Answer
                                                                     │
                                                                     ▼
                                                          Answer + Source Books
```

**Flow:** Question → LaBSE embedding → Qdrant vector search → Top 5 scripture passages → Ollama (Llama 3.1) → Answer with sources

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| OCR | Tesseract + pytesseract | Convert scanned Bengali PDFs to text |
| PDF Handling | pdf2image + Poppler | Convert PDF pages to images for OCR |
| Embeddings | LaBSE (SentenceTransformers) | Bengali-aware multilingual embeddings |
| Vector DB | Qdrant (Docker) | Store & search embeddings locally |
| Local LLM | Ollama + Llama 3.1 8B | Free, runs entirely on your machine |
| Backend | Python 3.11 + FastAPI | REST API for the RAG pipeline |
| Frontend | React + TailwindCSS | Devotee chat interface |
| Containerisation | Docker | Run Qdrant locally |

---

## 📁 Project Structure

```
Project_AT101/
├── venv/                        # Python virtual environment (not committed)
├── data/
│   ├── raw_pdfs/                # Scanned Bengali PDFs (not committed — large files)
│   ├── extracted_text/          # OCR output .txt files (not committed — large files)
│   └── chunks/
│       └── all_chunks.json      # Processed chunk data (not committed — large files)
├── ocr_extract.py               # Phase 2: OCR — converts scanned PDFs to text
├── chunk_data.py                # Phase 3: Cleans and chunks the Bengali text
├── index_chunks.py              # Phase 4: Generates embeddings and indexes to Qdrant
├── main.py                      # Phase 5: FastAPI RAG backend
├── requirements.txt             # Python dependencies
├── .env                         # API keys — never committed
├── .gitignore
└── frontend/                    # React chat interface
    ├── src/
    │   ├── App.js               # Main chat component
    │   └── index.css
    └── package.json
```

---

## ⚙️ Prerequisites

Make sure the following are installed on your machine before starting:

- [Homebrew](https://brew.sh) — macOS package manager
- [Python 3.11+](https://www.python.org/downloads/)
- [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/) with Bengali language pack (`tesseract-lang`)
- [Poppler](https://poppler.freedesktop.org) — for PDF processing
- [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/) — for running Qdrant
- [Ollama](https://ollama.com) — for running the local LLM
- [Node.js 18+](https://nodejs.org) — for the React frontend

---

## 🚀 Getting Started (Local Setup)

### 1. Clone the repository

```bash
git clone https://github.com/gourab98/Project_AT101.git
cd Project_AT101
```

### 2. Set up the Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Pull the Qdrant Docker image

```bash
docker pull qdrant/qdrant
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

### 4. Pull the Ollama LLM model

```bash
# For 16 GB RAM
ollama pull llama3.1

# For 8 GB RAM (use the smaller model)
ollama pull llama3.2
```

### 5. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 6. Add your Bengali PDF books

Place all scanned Bengali PDF files inside:
```
data/raw_pdfs/
```
Name them consistently, e.g., `book_001.pdf`, `book_002.pdf`, etc.

### 7. Run the data pipeline (one-time setup)

```bash
# Step 1: Extract text from scanned PDFs using OCR
python3 ocr_extract.py

# Step 2: Clean and chunk the extracted text
python3 chunk_data.py

# Step 3: Generate embeddings and index into Qdrant
python3 index_chunks.py
```

> ⚠️ OCR for 125+ books may take several hours. The script automatically skips already-processed books if restarted.

---

## ▶️ Starting the Project

Run each step in order, in separate terminal windows:

**Terminal 1 — Open Docker Desktop first, then start Qdrant:**
```bash
docker start qdrant
# Verify: http://localhost:6333/dashboard
```

**Terminal 2 — Start Ollama:**
```bash
ollama serve &
```

**Terminal 3 — Start the FastAPI backend:**
```bash
cd Project_AT101
source venv/bin/activate
uvicorn main:app --reload --port 8000
# Verify: http://127.0.0.1:8000/docs
```

**Terminal 4 — Start the React frontend:**
```bash
cd Project_AT101/frontend
npm start
# Opens automatically at: http://localhost:3000
```

---

## ⏹️ Stopping the Project

Stop in this order:

```bash
# 1. Stop FastAPI backend
Ctrl + C   # in the uvicorn terminal

# 2. Deactivate virtual environment
deactivate

# 3. Stop Ollama
pkill ollama

# 4. Stop React frontend
Ctrl + C   # in the npm terminal

# 5. Stop Qdrant
docker stop qdrant

# 6. Close Docker Desktop manually
```

---

## 🧪 Testing the API

Once the backend is running, open the interactive API docs:
```
http://127.0.0.1:8000/docs
```

Or test via curl:
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the guru say about devotion?"}'
```

Expected response:
```json
{
  "answer": "...",
  "sources": ["book_012", "book_047"]
}
```

---

## 📦 Updating GitHub

After making changes to your code:

```bash
git add .
git commit -m "Brief description of what you changed"
git push
```

---

## 🙏 Resource

Scripture source: [Sri Sri Thakur's Literature](https://srisrithakuranukulchandra.com/download-categories/original-sri-sri-thakurs-literature/)

---

## 📄 License

This project is for personal and devotional use. All scripture content belongs to the respective rights holders.
