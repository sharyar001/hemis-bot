import os
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! Railway yoki .env faylga qo‘shing.")

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Pasport seriya va raqamingizni yuboring (masalan: AA1234567 123456789)"
    )

# Foydalanuvchi xabarini qabul qilish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        series, number = text.split()
    except:
        await update.message.reply_text(
            "Iltimos, Pasport seriya va raqamini shunday yuboring: AA1234567 123456789"
        )
        return

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT HEMIS_ID, password FROM users WHERE passport_series=? AND passport_number=?",
        (series, number),
    )
    row = cur.fetchone()
    conn.close()

    if row:
        HEMIS_ID, password = row
        await update.message.reply_text(f"HEMIS ID: {HEMIS_ID}\nParol: {password}")
    else:
        await update.message.reply_text("Foydalanuvchi topilmadi ❌")

# Bot ishga tushirish
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

app.run_polling()
