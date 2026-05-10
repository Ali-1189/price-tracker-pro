import requests, pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

TOKEN = "8611242100:AAH5qOrYHbnKv9psVh7pAdbmAalalukqxUg"
CHAT_ID = "5637195275"

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)

driver.get("https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")
laptops = driver.find_elements(By.CLASS_NAME, "caption")

data = []
for laptop in laptops[:10]:
    name = laptop.find_element(By.CLASS_NAME, "title").text
    price = laptop.find_element(By.CLASS_NAME, "price").text
    data.append({"Product": name, "Price": price})

# حفظ في Excel
df = pd.DataFrame(data)
df.to_excel("leads.xlsx", index=False)

# إرسال تنبيه بسيط
requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
              data={"chat_id": CHAT_ID, "text": f"✅ تم سحب {len(data)} منتج وحفظهم في ملف leads.xlsx"})

driver.quit()
