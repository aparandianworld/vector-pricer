from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from config.settings import settings

def ingest_vectors():
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.openai_api_key,
        openai_api_base=settings.openai_base_url,
        model=settings.openai_model,
    )
    docs = [
        Document(page_content = "MacBook Air features: 13-inch display, M2 chip, 8GB RAM, 256GB storage, $999"),
        Document(page_content = "MacBook Pro features: 16-inch display, M3 chip, 16GB RAM, 512GB storage, $1999"),
    ]

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(settings.vector_db_path)
    print("Vectors with sample data ingested successfully.")

if __name__ == "__main__":
    ingest_vectors()