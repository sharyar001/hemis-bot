import telebot
import pandas as pd
import os

# Tokenni environmentdan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

CSV_FILE = "users.csv"

def load_data():
    return pd.read_csv(CSV_FILE)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Assalomu alaykum!\nPasport seriya va raqamingizni yuboring (masalan: AB1234567).")

@bot.message_handler(func=lambda message: True)
def send_credentials(message):
    passport = message.text.strip().upper()
    try:
        df = load_data()
        user = df[df['passport'] == passport]

        if not user.empty:
            hemis_id = user.iloc[0]['hemis_id']
            password = user.iloc[0]['password']
            bot.reply_to(message, f"✅ HEMIS ID: {hemis_id}\n🔑 Parol: {password}")
        else:
            bot.reply_to(message, "❌ Bunday pasport topilmadi.")
    except Exception as e:
        bot.reply_to(message, f"Xatolik: {e}")

print("🤖 Bot ishga tushdi...")
bot.infinity_polling()
