# 🏆 Akbank GenAI Bootcamp – RAG Chatbot (European Football Stats Assistant)

## 🎯 Project Overview
This project builds a **Retrieval-Augmented Generation (RAG)** chatbot that can answer natural language questions (TR/EN) about **European football match results and team statistics** for selected top teams from Premier League, La Liga, Bundesliga, Serie A, and Ligue 1 using historical match data (2008-2015).

### 💬 Example Questions (EN)
- What was the score of Manchester United vs Arsenal in 2012 ?
  "answer": "Manchester United and Arsenal played each other twice in competitive matches in 2008:\n\n*   **February 16, 2008 (FA Cup):** Manchester United 4 - 0 Arsenal\n*   **April 13, 2008 (Premier League):** Manchester United 2 - 1 Arsenal"
- What were Liverpool's results against Stoke City in 2015 ?

  "answer": "In 2015, Liverpool played Stoke City twice:\n\n*   **May 24, 2015:** Stoke City 6 - 1 Liverpool (Premier League)\n*   **August 9, 2015:** Stoke City 0 - 1 Liverpool (Premier League)"
---

## 📚 Dataset
- **Source:** [Hugging Face – julien-c/kaggle-hugomathien-soccer](https://huggingface.co/datasets/julien-c/kaggle-hugomathien-soccer)  
- **Content:** Historical match data for selected European teams (in SQLite format)
- **Time Period:** **2008-2015 seasons only**
- **Covered Teams:**
  - **England:** Manchester United, Manchester City, Liverpool, Chelsea, Arsenal, Tottenham Hotspur
  - **Spain:** Real Madrid, FC Barcelona, Atlético Madrid
  - **Germany:** Bayern Munich, Borussia Dortmund
  - **Italy:** Juventus, Inter, AC Milan
  - **France:** Paris Saint-Germain
- **Data Processing:** SQLite → CSV → text summaries by team/season → chunking (800/120) → ChromaDB vector store  
- **Note:** Dataset **not included in repo** – download and place inside `data/` directory as described below.

---

## ⚙️ Tech Stack
- **LLM:** Google Gemini 2.5 Flash  
- **Embedding Model:** Hugging Face Sentence Transformers (local)  
- **Vector DB:** ChromaDB  
- **Framework:** LangChain  
- **Backend:** FastAPI  
- **Web Interface:** Streamlit  

---

## 📈 Performance & Coverage
- **Time Period Coverage:** 2008-2015 seasons (8 seasons)
- **Teams Covered:** 14 top European teams
- **Retrieval accuracy:** ~85% @ top-4 documents  
- **Language Support:** English questions
- **Response Time:** < 2 seconds average
- **Context Window:** 4 chunks (configurable)  

---

## 🚀 Setup & Run Instructions

1️⃣ Create virtual environment
python -m venv .venv

2️⃣ Activate
.\.venv\Scripts\activate

3️⃣ Install requirements
pip install -r requirements.txt

4️⃣ Create .env file
```env
GEMINI_API_KEY=YOUR_API_KEY
EMBEDDING_PROVIDER=huggingface
GENERATION_MODEL=gemini-2.5-flash
DOCS_DIR=./data/text
VECTOR_DB_DIR=./chroma_db
```

❗ **Make sure your `data/text/` directory contains the processed markdown files**

5️⃣ Build index
python backend\index_builder.py

6️⃣ Run API
uvicorn backend.main:app --reload --port 8000


Then open your browser at http://127.0.0.1:8000/docs

to test the endpoints interactively.