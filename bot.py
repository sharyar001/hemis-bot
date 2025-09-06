import telebot
import pandas as pd

# Bot tokenini bu yerga yozing
BOT_TOKEN = "7502234027:AAEns2AjMhEEBv6AmTVUFE9gdBKVFV4aloQ"
bot = telebot.TeleBot(BOT_TOKEN)

# CSV fayl manzili
CSV_FILE = "users.csv"

def load_data():
    return pd.read_csv(CSV_FILE)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 
                 "Assalomu alaykum!\n\n"
                 "Pasport seriya va raqamingizni yuboring (masalan: AB1234567).\n"
                 "Men sizga HEMIS ID va parolingizni chiqarib beraman ✅")

@bot.message_handler(func=lambda message: True)
def send_credentials(message):
    passport = message.text.strip().upper()
    
    try:
        df = load_data()

        # Foydalanuvchini qidirish
        user = df[df['passport'] == passport]

        if not user.empty:
            hemis_id = user.iloc[0]['hemis_id']
            password = user.iloc[0]['password']

            bot.reply_to(message, f"✅ Ma'lumot topildi:\n\n"
                                  f"📌 HEMIS ID: {hemis_id}\n"
                                  f"🔑 Parol: {password}")
        else:
            bot.reply_to(message, "❌ Bunday pasport raqami topilmadi. Iltimos tekshirib qaytadan yuboring.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Xatolik yuz berdi: {e}")

print("🤖 Bot ishga tushdi...")
bot.infinity_polling()
