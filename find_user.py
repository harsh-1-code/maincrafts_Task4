import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Fetch all usernames
cursor.execute("SELECT username FROM users")
users = cursor.fetchall()

print("--- REGISTERED USERNAMES ---")
for user in users:
    print(f"👤 {user[0]}")
print("----------------------------")

conn.close()