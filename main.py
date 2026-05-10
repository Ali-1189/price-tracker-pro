import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# استيراد الملفات اللي نظفناها سوا
from app.scraper.scraper import Scraper
from app.scraper.parser import PriceParser
from app.database.db import init_db, save_price

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if "amazon.eg" not in url.lower():
        await update.message.reply_text("❌ حالياً بدعم أمازون مصر بس، ابعت لينك صحيح.")
        return

    await update.message.reply_text("⏳ ثواني، بجيب لك السعر حالاً...")
    
    try:
        # التصحيح: شيلنا الـ with واستخدمنا fetch_url
        scraper = Scraper()
        html = scraper.fetch_url(url)
        
        if html:
            current_price = PriceParser.parse_amazon_price(html)
            
            if current_price:
                # حفظ في القاعدة
                save_price("منتج أمازون", url, current_price)
                await update.message.reply_text(f"✅ تم! السعر الحالي: *{current_price}* جنيه.", parse_mode="Markdown")
            else:
                await update.message.reply_text("⚠️ السعر مش راضي يظهر، ممكن أمازون عاملة حماية. جرب كمان شوية.")
        else:
            await update.message.reply_text("❌ فشلت في فتح الصفحة، اتأكد من اللينك.")
            
    except Exception as e:
        await update.message.reply_text(f"❌ حصلت مشكلة: {e}")

if __name__ == "__main__":
    init_db()
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))
    print("🚀 البوت شغال دلوقتي.. روح جربه!")
    app.run_polling()
    