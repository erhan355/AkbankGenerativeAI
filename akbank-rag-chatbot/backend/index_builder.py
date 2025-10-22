"""
Basit komut satırı script'i:
python backend/index_builder.py
"""

from rag_pipeline import build_or_load_vectorstore

if __name__ == "__main__":
    print("🔧 Chroma vektör veritabanı oluşturuluyor veya yükleniyor...")
    vectordb = build_or_load_vectorstore()
    print("✅ Chroma index hazır.")
    print(f"📂 Persist directory: {vectordb._persist_directory}")
    print("İlk çalıştırmada embed işlemi biraz sürebilir (doküman sayısına göre).")
