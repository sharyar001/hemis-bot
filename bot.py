import os
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Token va URL muhitdan olinadi
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")  # masalan: https://hemis-bot-production.up.railway.app

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! Railway Variables bo‘limida BOT_TOKEN qo‘ying.")
if not RAILWAY_URL:
    raise ValueError("❌ RAILWAY_URL topilmadi! Railway Variables bo‘limida RAILWAY_URL qo‘ying.")

# 📌 START komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Pasport seriya va raqamingizni yuboring.\n\n"
        "Masalan: AD1234567"
    )

# 📌 Pasport qidirish funksiyasi
async def search_passport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().upper()

    # Pasport formati tekshirish
    if len(user_input) != 9 or not user_input[:2].isalpha() or not user_input[2:].isdigit():
        await update.message.reply_text("❌ Noto‘g‘ri format! Masalan: AD1234567")
        return

    # 🔎 SQLite bazadan qidirish
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT hemis_id, password FROM users WHERE passport=?", (user_input,))
    result = cursor.fetchone()
    conn.close()

    if result:
        hemis_id, password = result
        await update.message.reply_text(
            f"✅ Topildi!\n\n🆔 HEMIS ID: {hemis_id}\n🔑 Parol: {password}"
        )
    else:
        await update.message.reply_text("❌ Bunday pasport bazada topilmadi!")

# 📌 Asosiy app
app = Application.builder().token(BOT_TOKEN).build()

# Handlerlar
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_passport))

# 🚀 Webhook rejimida ishga tushirish
if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        url_path=BOT_TOKEN,
        webhook_url=f"{RAILWAY_URL}/{BOT_TOKEN}"
    )
