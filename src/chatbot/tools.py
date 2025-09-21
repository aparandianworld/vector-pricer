from langchain.tools import tool
import sqlite3
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from config.settings import settings


@tool
def get_product_price(laptop_name: str) -> str:
    conn = sqlite3.connect(settings.postgres_url.replace("sqlite://", ""))
    c = conn.cursor()
    c.execute("SELECT price FROM laptops WHERE name = ?", (laptop_name,))
    result = c.fetchone()
    conn.close()
    if result:
        return f"The price of {laptop_name} is: ${result[0]}."
    else:
        return f"Price for {laptop_name} not found."

@tool
def get_product_features(laptop_name: str) -> str:
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    vectorstore = FAISS.load(
        settings.vector_db_path, 
        embeddings,
        allow_dangerous_deserialization = True # safe for local development
    )
    results = vectorstore.similarity_search(f"Features of product {laptop_name}", k = 1)
    return results[0].page_content if results else f"Features for {laptop_name} not found."