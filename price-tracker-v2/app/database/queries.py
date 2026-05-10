import sqlite3

def insert_price(conn, product_name, url, price):
    # الداتا بيز هتحط الـ timestamp لوحدها فبنبعت الـ 3 قيم دول بس
    query = "INSERT INTO prices (product_name, url, price) VALUES (?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, (product_name, url, price))
    conn.commit()

def get_last_price(conn, url):
    # التعديل: بنرتب حسب الـ id تنازلياً عشان نضمن نجيب أحدث سعر متسجل
    query = "SELECT price FROM prices WHERE url = ? ORDER BY id DESC LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(query, (url,))
    result = cursor.fetchone()
    return result[0] if result else None