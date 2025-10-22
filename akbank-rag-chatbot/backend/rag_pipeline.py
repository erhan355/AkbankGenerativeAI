import os
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
load_dotenv()

# LangChain + Gemini
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.schema import Document

# ==== ENV ====
GEMINI_API_KEY   = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL  = os.getenv("EMBEDDING_MODEL", "text-embedding-004")
GENERATION_MODEL = os.getenv("GENERATION_MODEL", "gemini-1.5-flash")
DOCS_DIR         = os.getenv("DOCS_DIR", "./data/text")
VECTOR_DB_DIR    = os.getenv("VECTOR_DB_DIR", "./chroma_db")

# ==== Loader ====
def load_text_documents(docs_dir: str | Path) -> List[Document]:
    """
    DOCS_DIR içindeki .md / .txt dosyalarını LangChain Document listesine çevirir.
    """
    base = Path(docs_dir)
    if not base.exists():
        raise FileNotFoundError(f"DOCS_DIR not found: {base}")

    docs: List[Document] = []
    for ext in ("*.md", "*.txt"):
        for fp in base.rglob(ext):
            loader = TextLoader(str(fp), encoding="utf-8")
            docs.extend(loader.load())
    if not docs:
        raise RuntimeError(f"No .md/.txt files found under {base}. Did you run the extraction script?")
    return docs

# ==== Build / Load Vector DB ====
def build_or_load_vectorstore() -> Chroma:
    """
    Varsa Chroma'yı yükler; yoksa DOCS_DIR'den belgeleri okuyup oluşturur.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=GEMINI_API_KEY)

    # Eğer indeks klasörü doluysa direkt yükle
    if os.path.exists(VECTOR_DB_DIR) and os.listdir(VECTOR_DB_DIR):
        return Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)

    # Yeni indeks inşası
    docs = load_text_documents(DOCS_DIR)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)

    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=VECTOR_DB_DIR)
    vectordb.persist()
    return vectordb

# ==== RAG Chain ====
def get_qa_chain() -> RetrievalQA:
    """
    RetrievalQA chain (stuff) döndürür. .run(question) ile cevap üretir.
    """
    vectordb = build_or_load_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    llm = ChatGoogleGenerativeAI(model=GENERATION_MODEL, temperature=0.2, google_api_key=GEMINI_API_KEY)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
    return qa

# ==== Yardımcılar (opsiyonel) ====
def answer(question: str) -> str:
    """Soruya kısa yanıt döndürür (string)."""
    chain = get_qa_chain()
    return chain.run(question)

def retrieve_sources(question: str) -> List[Dict[str, Any]]:
    """
    En ilgili kaynak chunk'larını döndürür (metin + metadata + skor yok; skor için Chroma raw çağrısı gerekir).
    UI'da kaynak göstermek istersen işe yarar.
    """
    vectordb = build_or_load_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    docs = retriever.get_relevant_documents(question)
    return [{"content": d.page_content, "meta": d.metadata} for d in docs]
def top_k_sources(question: str, k: int = 4):
    """
    Soru için en ilgili k dokümanı döndürür.
    Document listesi döner; main.py içinde content/metadata'ya erişiyoruz.
    """
    vectordb = build_or_load_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    return retriever.get_relevant_documents(question)
