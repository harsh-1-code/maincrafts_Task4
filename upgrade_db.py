import sqlite3

# Connect to your existing database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 1. Add the 'role' column (The try/except prevents errors if you run this twice)
try:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    print("Success: Added 'role' column to the users table.")
except sqlite3.OperationalError:
    print("Note: 'role' column already exists.")

# 2. Promote a specific user to admin
# CHANGE THIS to the username you registered with in Task 2!
admin_username = 'admin' 

cursor.execute("UPDATE users SET role = 'admin' WHERE username = ?", (admin_username,))
conn.commit()

print(f"Success: Promoted '{admin_username}' to admin status!")
conn.close()