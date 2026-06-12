import sqlite3

# Connect to the database (this creates it if it doesn't exist)
conn = sqlite3.connect("database.db")

# 1. Create the users table (from Task 2)
conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')

# 2. Create the students table (from Task 3)
conn.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        course TEXT
    )
''')

print("Database fully initialized with users and students tables!")
conn.close()