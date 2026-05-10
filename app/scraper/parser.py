from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)

class PriceParser:
    @staticmethod
    def parse_amazon_price(html_content):
        if not html_content:
            return None
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. قائمة selectors شاملة لأمازون مصر
        selectors = [
            '.a-price-whole', 
            '.a-offscreen', 
            '#priceblock_ourprice', 
            '#price_inside_buybox',
            '#kindle-price'
        ]
        
        for s in selectors:
            el = soup.select_one(s)
            if el:
                text = el.get_text().replace('٫', '.').replace(',', '').strip()
                # استخراج الرقم فقط (بيشيل "جنيه" أو "EGP")
                numbers = re.findall(r'\d+\.?\d*', text)
                if numbers:
                    try:
                        return float(numbers[0])
                    except: continue
        
        # 2. حل احتياطي لو السيلكتورز فشلت (بيدور في الـ Meta)
        meta_price = soup.find("meta", {"property": "og:title"})
        if meta_price and "EGP" in meta_price['content']:
            res = re.findall(r'\d+\.?\d*', meta_price['content'].replace(',', ''))
            if res: return float(res[0])
            
        return None