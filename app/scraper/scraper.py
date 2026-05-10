import requests
import time
import random
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class Scraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/"
        }

    def fetch_url(self, url):
        try:
            # تأخير عشوائي عشان أمازون متقفشوش
            time.sleep(random.uniform(1.5, 3.5))
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"Failed to fetch {url}. Status: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching URL: {e}")
            return None