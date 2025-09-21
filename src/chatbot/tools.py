from langchain.tools import tool
import sqlite3
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from config.settings import settings


@tool
def get_product_price(product_name: str) -> str:
    """Given a product name, returns the price from RDBMS."""
    conn = sqlite3.connect(settings.postgres_url.replace("sqlite:///", ""))
    c = conn.cursor()
    c.execute("SELECT price FROM laptops WHERE name = ?", (product_name,))
    result = c.fetchone()
    conn.close()
    if result:
        return f"The price of {product_name} is: ${result[0]}."
    else:
        return f"Price for {product_name} not found."

@tool
def get_product_features(product_name: str) -> str:
    """Given a product name, returns features from VectorDB."""
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.openai_api_key,
        model = "text-embedding-3-small"
    )
    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings=embeddings, 
        allow_dangerous_deserialization=True
    )
    results = vectorstore.similarity_search(f"Features of product {product_name}", k = 1)
    return results[0].page_content if results else f"Features for {product_name} not found."