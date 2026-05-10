import sqlite3
from pathlib import Path

# تحديد المسار النسبي عشان يشتغل على أي جهاز
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data"
DB_PATH.mkdir(exist_ok=True)
DATABASE_FILE = DB_PATH / "prices.db"

def get_connection():
    return sqlite3.connect(DATABASE_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            url TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_price(product_name, url, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prices (product_name, url, price) VALUES (?, ?, ?)", 
                   (product_name, url, price))
    conn.commit()
    conn.close()