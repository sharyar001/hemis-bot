import os
import telebot
import pandas as pd
from dotenv import load_dotenv

# .env fayldan tokenni olish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! Railway yoki .env faylga qo‘shing.")

# Botni ishga tushirish
bot = telebot.TeleBot(BOT_TOKEN)

# CSV faylni o‘qish (users.csv)
DATA_FILE = "users.csv"

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError("❌ users.csv fayl topilmadi!")

users_df = pd.read_csv(DATA_FILE)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Assalomu alaykum!\n\n"
        "Pasport seriya va raqamingizni yuboring (masalan: AA1234567), "
        "men sizga HEMIS ID va parolingizni qaytaraman."
    )

# Foydalanuvchi yuborgan xabarni qayta ishlash
@bot.message_handler(func=lambda message: True)
def send_credentials(message):
    passport = message.text.strip().upper()

    # users.csv ichidan qidirish
    user = users_df[users_df['passport'] == passport]

    if not user.empty:
        hemis_id = user.iloc[0]['hemis_id']
        password = user.iloc[0]['password']
        bot.reply_to(
            message,
            f"✅ Ma'lumot topildi:\n\n"
            f"📌 HEMIS ID: {hemis_id}\n"
            f"🔑 Parol: {password}"
        )
    else:
        bot.reply_to(
            message,
            "❌ Bunday pasport topilmadi. Iltimos, ma’lumotni to‘g‘ri kiriting."
        )

# Botni ishga tushirish
print("🤖 Bot ishga tushdi...")
bot.infinity_polling()
