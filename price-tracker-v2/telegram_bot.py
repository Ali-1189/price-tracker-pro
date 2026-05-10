import requests
from bs4 import BeautifulSoup

TOKEN = "8611242100:AAH5qOrYHbnKv9psVh7pAdbmAalalukqxUg"
CHAT_ID = "5637195275"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

url = "https://books.toscrape.com/"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

message = "📚 أحدث الكتب:\n\n"
for book in soup.find_all("article", class_="product_pod")[:5]:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text.strip()
    message += f"📖 {title}\n💰 {price}\n\n"

send_message(message)
print("تم الإرسال!")
