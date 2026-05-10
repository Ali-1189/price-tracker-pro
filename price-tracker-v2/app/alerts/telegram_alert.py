import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

# إعداد اللوجر
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على أمر /start"""
    await update.message.reply_text(
        "👋 أهلاً بك في بوت صائد الأسعار!\n\n"
        "أرسل لي رابط المنتج من (أمازون، نون، جوميا) وسأقوم بمراقبته فوراً."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """التعامل مع الروابط المرسلة"""
    url = update.message.text
    # هنا هننادي على المنطق بتاع الـ Scraper (هنربطه في الخطوة الجاية)
    await update.message.reply_text(f"⏳ جاري فحص الرابط ومبدأ المراقبة...\n{url}")

def run_bot():
    """تشغيل البوت"""
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

# دالة قديمة للرسائل الخام (للخلفية)
def send_price_alert_raw(text):
    # كود الإرسال السريع اللي عملناه قبل كدة
    import requests
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})