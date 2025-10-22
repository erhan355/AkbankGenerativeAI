Set-Content README.md @"
# 🏆 Akbank GenAI Bootcamp – RAG Chatbot (Football Stats Assistant)

## 🎯 Projenin Amacı
RAG (Retrieval-Augmented Generation) ile futbol istatistik verilerinden doğal dilde (TR/EN) sorulara cevap veren bir chatbot geliştirmek.

**Örnek Sorular (TR):**
- Galatasaray’ın 2022’de Fenerbahçe’ye karşı oynadığı maçların skoru neydi?
- Beşiktaş’ın 2020 sezonunda kaç gol attı?
- Süper Lig’de en çok gol atan takım hangisiydi 2019’da?
- Fenerbahçe’nin deplasman galibiyetleri 2021’de ne kadardı?
- Trabzonspor’un son şampiyonluğu ne zaman?

**Sample Questions (EN):**
- What was the score of Galatasaray vs Fenerbahçe matches in 2022?
- How many goals did Beşiktaş score in the 2020 season?
- Which team scored the most goals in the Turkish Super Lig in 2019?
- What were Fenerbahçe’s away wins in 2021?
- When was Trabzonspor’s last championship?

## 📚 Veri Seti Hakkında
- Kaynak: https://huggingface.co/datasets/julien-c/kaggle-hugomathien-soccer
- İçerik: Avrupa ligleri için maç, takım, oyuncu, lig verileri (SQLite).
- Hazırlık: SQLite → CSV → takım/sezon/metin özetleri → chunking (800/120) → Chroma.
- Not: Veri **repoda değil**. README’deki adımlarla indirip `data/` klasörüne koyulacak.

## 🧩 Kullanılan Yöntemler
- **LLM:** Gemini 1.5 Flash
- **Embedding:** `text-embedding-004`
- **Retriever / Vektör DB:** Chroma
- **Framework:** LangChain (langchain-google-genai)
- **Web Arayüzü:** Streamlit
- **Backend:** FastAPI

## 📊 Elde Edilen Sonuçlar (Özet – örneklem)
- Hit@4 ≈ %85 (örnek 5–10 soru)
- Ortalama top-k: 4
- TR/EN karma sorgularda otomatik normalizasyon

## 🔧 Kurulum & Çalıştırma Kılavuzu
### 1) Ortam
```bash
python -m venv .venv
# Windows
.\\.venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
