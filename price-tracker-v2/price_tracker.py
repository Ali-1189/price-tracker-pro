import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")

with open("books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price"])
    for book in books[:5]:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        writer.writerow([title, price])

print("Done! books.csv saved.")
