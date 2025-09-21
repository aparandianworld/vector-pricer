import sqlite3
from config.settings import settings

def setup_rdbms():
    conn = sqlite3.connect(settings.postgres_url.replace("sqlite:///", ""))
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS laptops (name TEXT PRIMARY KEY, price REAL)
        ''')
    laptops = [
        ("MacBook Air", 999),
        ("MacBook Pro", 1999),
    ]
    c.executemany("INSERT INTO laptops VALUES (?, ?)", laptops)
    conn.commit()
    conn.close()
    print("RDBMS set up complete with sample data.")

if __name__ == "__main__":
    setup_rdbms()