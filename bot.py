import os
import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! Railway yoki .env faylga qo‘shing.")

# /start komandasi
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom! Pasport seriya va raqamingizni yuboring (masalan: AA1234567 123456789)")

# Foydalanuvchi xabarini qabul qilish
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    try:
        series, number = text.split()
    except:
        update.message.reply_text("Iltimos, Pasport seriya va raqamini shunday yuboring: AA1234567 123456789")
        return

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT HEMIS_ID, password FROM users WHERE passport_series=? AND passport_number=?", (series, number))
    row = cur.fetchone()
    conn.close()

    if row:
        HEMIS_ID, password = row
        update.message.reply_text(f"HEMIS ID: {HEMIS_ID}\nParol: {password}")
    else:
        update.message.reply_text("Foydalanuvchi topilmadi ❌")

# Bot ishga tushirish
updater = Updater(BOT_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
updater.idle()
