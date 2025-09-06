import pandas as pd
import sqlite3

csv_file = "users.csv"

# CSV faylni o‘qish
df = pd.read_csv(csv_file)

# SQLite bazasi
conn = sqlite3.connect("users.db")
df.to_sql("users", conn, if_exists="replace", index=False)
conn.close()

print("✅ CSV ma’lumotlari bazaga import qilindi")
