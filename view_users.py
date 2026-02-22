import sqlite3

# Connect to your database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Fetch all users
cursor.execute("SELECT id, username, full_name FROM users")
users = cursor.fetchall()

conn.close()

# Print all users
print("ID | Username | Full Name")
print("-------------------------")
for user in users:
    print(f"{user[0]} | {user[1]} | {user[2]}")