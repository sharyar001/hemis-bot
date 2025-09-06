import os
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Pasport seriya va raqamingizni yuboring (masalan: AA1234567)"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    passport = update.message.text.strip()  # endi butun ketma-ket pasport

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT HEMIS_ID, password FROM users WHERE passport=?",
        (passport,),
    )
    row = cur.fetchone()
    conn.close()

    if row:
        HEMIS_ID, password = row
        await update.message.reply_text(f"HEMIS ID: {HEMIS_ID}\nParol: {password}")
    else:
        await update.message.reply_text("Foydalanuvchi topilmadi ❌")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

app.run_polling()
