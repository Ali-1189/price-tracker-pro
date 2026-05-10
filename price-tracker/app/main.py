import os
from dotenv import load_dotenv # أضف ده
load_dotenv() # وأضف ده كمان
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from app.scraper.scraper import Scraper
from app.scraper.parser import PriceParser
from app.scraper.selectors import SITE_CONFIGS
from app.database.db import get_connection, init_db
from app.database.queries import insert_price, get_last_price
from app.alerts.message_builder import build_price_alert

logging.basicConfig(level=logging.INFO)

def get_site_config(url):
    for domain, config in SITE_CONFIGS.items():
        if domain in url.lower(): return config
    return None

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    config = get_site_config(url)
    
    if not config:
        await update.message.reply_text("❌ الموقع ده لسه مش مدعوم، ابعت لينك أمازون أو نون أو جوميا.")
        return

    await update.message.reply_text("⏳ ثواني، بجيب لك السعر حالاً...")
    
    try:
        with Scraper() as scraper:
            html = scraper.fetch(url)
            parser = PriceParser(selector=config["price"])
            current_price = parser.extract_price(html)

        if current_price:
            conn = get_connection()
            old_price = get_last_price(conn, url)
            insert_price(conn, "Product", url, current_price)
            msg = build_price_alert("منتج من الرابط", current_price, url, old_price)
            await update.message.reply_text(msg, parse_mode="Markdown")
            conn.close()
        else:
            await update.message.reply_text("⚠️ مش عارف أوصل للسعر، جرب لينك تاني.")
    except Exception as e:
        await update.message.reply_text(f"❌ حصلت مشكلة: {e}")

if __name__ == "__main__":
    init_db()
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))
    print("🚀 البوت شغال دلوقت.. جربه من الموبايل!")
    app.run_polling()