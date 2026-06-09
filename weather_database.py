import pandas as pd
import sqlite3

conn = sqlite3.connect("weather.db")

df = pd.read_csv("cleaned_weather.csv")

df.to_sql(
    "weather",
    conn,
    if_exists="replace",
    index=False
)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM weather")

print("Rows in database:", cursor.fetchone()[0])

print("\nFirst 5 Records:")

cursor.execute("SELECT * FROM weather LIMIT 5")

for row in cursor.fetchall():
    print(row)

# ----------------------------------
# Database Queries
# ----------------------------------

cursor.execute("""
SELECT City, Temperature
FROM weather
ORDER BY Temperature DESC
LIMIT 5
""")

print("\nTop 5 Hottest Cities:")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
SELECT City, Temperature
FROM weather
ORDER BY Temperature ASC
LIMIT 5
""")

print("\nTop 5 Coolest Cities:")
for row in cursor.fetchall():
    print(row)

conn.close()