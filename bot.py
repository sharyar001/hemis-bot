import telebot
import pandas as pd
import os

# Tokenni environmentdan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Tokenni logga chiqarib ko‘rish (Railway Logs da ko‘rasiz)
print("BOT_TOKEN qiymati:", BOT_TOKEN)

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi. Railway Variables ga token qo‘shganingizni tekshiring.")

# Botni ishga tushirish
bot = telebot.TeleBot(BOT_TOKEN)

# CSV fayl manzili
CSV_FILE = "users.csv"

def load_data():
    return pd.read_csv(CSV_FILE)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(
        message,
        "Assalomu alaykum!\n\n"
        "Pasport seriya va raqamingizni yuboring (masalan: AB1234567).\n"
        "Men sizga HEMIS ID va parolingizni yuboraman ✅"
    )

@bot.message_handler(func=lambda message: True)
def send_credentials(message):
    passport = message.text.strip().upper()
    try:
        df = load_data()
        user = df[df['passport'] == passport]

        if not user.empty:
            hemis_id = user.iloc[0]['hemis_id']
            password = user.iloc[0]['password']
            bot.reply_to(
                message,
                f"✅ Ma'lumot topildi:\n\n📌 HEMIS ID: {hemis_id}\n🔑 Parol: {pas_
