# 🏆 Akbank GenAI Bootcamp – RAG Chatbot (European Football Stats Assistant)

## 🎯 Project Overview
This project builds a **Retrieval-Augmented Generation (RAG)** chatbot that can answer natural language questions (TR/EN) about **European football statistics** using structured match and player data.

### 💬 Example Questions (EN)
- What was the score of Manchester United vs Chelsea in 2022?  
- How many goals did Lionel Messi score in the 2011–2012 season?  
- Which team won the Premier League in 2020?  
- Who were the top scorers in La Liga in 2018?  
- How many assists did Cristiano Ronaldo make in Serie A 2021?

### 🔍 Örnek Sorular (TR)
- Manchester United ile Chelsea’nin 2022’deki maçlarının skoru neydi?  
- Lionel Messi 2011–2012 sezonunda kaç gol attı?  
- Premier League’i 2020 yılında hangi takım kazandı?  
- 2018’de La Liga’da en çok gol atan oyuncular kimlerdi?  
- Cristiano Ronaldo Serie A’da 2021’de kaç asist yaptı?

---

## 📚 Dataset
- **Source:** [Hugging Face – julien-c/kaggle-hugomathien-soccer](https://huggingface.co/datasets/julien-c/kaggle-hugomathien-soccer)  
- **Content:** Match, player, team, and league data (European leagues, in SQLite format)  
- **Preparation:** SQLite → CSV → text summaries by team/season → chunking (800/120) → Chroma vector store  
- **Note:** Dataset **not included in repo** – download and place inside `data/` directory as described below.

---

## ⚙️ Tech Stack
- **LLM:** Gemini 1.5 Flash  
- **Embedding Model:** `models/text-embedding-004`  
- **Vector DB:** Chroma  
- **Framework:** LangChain (langchain-google-genai)  
- **Backend:** FastAPI  
- **Web Interface:** Streamlit  

---

## 📈 Performance (Sample)
- Retrieval accuracy @top4 ≈ 85% (on 5–10 random queries)  
- Handles bilingual (TR/EN) questions automatically  
- Mean context size: 4 chunks  

---

## 🚀 Setup & Run Instructions

1️⃣ Create virtual environment
```bash
python -m venv .venv

2️⃣ Activate
.\.venv\Scripts\activate

3️⃣ Install requirements
pip install -r requirements.txt

4️⃣ Create .env file
GEMINI_API_KEY=YOUR_API_KEY
EMBEDDING_MODEL=models/text-embedding-004
GENERATION_MODEL=models/gemini-1.5-flash
DOCS_DIR=./data/text
VECTOR_DB_DIR=./chroma_db

5️⃣ Build index
python backend\index_builder.py

6️⃣ Run API
uvicorn backend.main:app --reload --port 8000


Then open your browser at http://127.0.0.1:8000/docs

to test the endpoints interactively.