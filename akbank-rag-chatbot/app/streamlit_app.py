import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/ask")

st.set_page_config(page_title="Akbank RAG Chatbot", page_icon="⚽", layout="centered")

st.title("⚽ Akbank GenAI Bootcamp - RAG Chatbot")
st.markdown(
    "Bu chatbot, futbol istatistikleri veri seti üzerinde RAG (Retrieval-Augmented Generation) "
    "mimarisi ile geliştirilmiştir. Gemini API + ChromaDB + LangChain tabanlıdır."
)
st.divider()

question = st.text_area("🔍 Soru girin:", placeholder="Galatasaray 2022'de Fenerbahçe'ye karşı kaç gol attı?")
k_val = st.slider("Kaç belge getirilsin (k):", 2, 6, 4)
ask_button = st.button("Sor!")

if ask_button and question.strip():
    with st.spinner("Yanıt getiriliyor..."):
        try:
            resp = requests.post(API_URL, json={"question": question, "k": k_val})
            if resp.status_code == 200:
                st.success("✅ Yanıt hazır")
                st.write(resp.json()["answer"])
            else:
                st.error(f"Hata kodu: {resp.status_code}")
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")

st.caption("Developed for Akbank GenAI Bootcamp by [Your Name]")
