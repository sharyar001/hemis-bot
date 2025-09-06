import pandas as pd
import sqlite3

# CSV faylni o‘qish
df = pd.read_csv("users.csv")

# SQLite bilan bog‘lanish
conn = sqlite3.connect("users.db")
df.to_sql("users", conn, if_exists="replace", index=False)
conn.close()
print("✅ CSV ma’lumotlari bazaga import qilindi")
