import os
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")  # misol: https://hemis-bot-production.up.railway.app/

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi!")
if not RAILWAY_URL:
    raise ValueError("❌ RAILWAY_URL topilmadi!")

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Pasport seriya va raqamingizni yuboring (masalan: AD1234567)"
    )

# Foydalanuvchi xabarini qabul qilish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pasport seriya+raqamni tozalash
    passport = update.message.text.replace(" ", "").strip().upper()

    # Bazadan qidirish
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT HEMIS_ID, password FROM users WHERE passport=?", (passport,))
    row = cur.fetchone()
    conn.close()

    if row:
        HEMIS_ID, password = row
        await update.message.reply_text(f"✅ HEMIS ID: {HEMIS_ID}\n🔑 Parol: {password}")
    else:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi")

# Botni yaratish va handlerlarni qo‘shish
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# Webhook orqali ishlash
app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 8443)),
    webhook_url=RAILWAY_URL
)
