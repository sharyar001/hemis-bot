import csv
import sqlite3

# CSV fayldan bazaga yuklash
def import_csv_to_db(csv_file, db_file):
    # SQLite ulanish
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Agar users jadvali bo‘lmasa, yaratamiz
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passport TEXT UNIQUE,
            hemis_id TEXT,
            password TEXT
        )
    """)

    # CSV ochamiz va bazaga yozamiz
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            passport = row["passport"].strip().upper()
            hemis_id = row["hemis_id"].strip()
            password = row["password"].strip()

            cursor.execute("""
                INSERT OR REPLACE INTO users (passport, hemis_id, password)
                VALUES (?, ?, ?)
            """, (passport, hemis_id, password))

    # Saqlaymiz va yopamiz
    conn.commit()
    conn.close()
    print("✅ CSV fayldan ma’lumotlar bazaga muvaffaqiyatli yuklandi!")

# Asosiy ishga tushirish
if __name__ == "__main__":
    import_csv_to_db("users.csv", "users.db")
