# database.py
import sqlite3

def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            phone_number TEXT PRIMARY KEY,
            session_id TEXT,
            forward_rules TEXT  -- Store forward rules as JSON
        )
    ''')
    conn.commit()
    conn.close()

def add_user(phone_number, session_id, forward_rules):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (phone_number, session_id, forward_rules) VALUES (?, ?, ?)",
                   (phone_number, session_id, forward_rules))
    conn.commit()
    conn.close()

def get_user(phone_number):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, forward_rules FROM users WHERE phone_number = ?", (phone_number,))
    result = cursor.fetchone()
    conn.close()
    return result

# Add functions to update forward rules, etc.