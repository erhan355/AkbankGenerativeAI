from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.rag_pipeline import answer, top_k_sources

app = FastAPI(title="Akbank RAG Chatbot")

# Gerekirse CORS'u aç
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # prod'da domain ile sınırla
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    k: int = 4  # kaç bağlam döndürelim (opsiyonel)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(q: Query):
    """Sadece yanıt döndürür."""
    # k parametresini göndermiyoruz; answer(question) imzasına uyuyor
    ans = answer(q.question)
    return {"answer": ans}


@app.post("/ask_with_sources")
def ask_with_sources(q: Query):
    """Yanıt + kaynak pasajları döndürür (UI'da göstermek için)."""
    srcs = top_k_sources(q.question, k=q.k)
    ans = answer(q.question, k=q.k)
    # küçük bir normalize
    sources = [{"content": d.page_content, "metadata": d.metadata} for d in srcs]
    return {"answer": ans, "sources": sources}
