# database.py
import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

def create_table():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            phone_number TEXT PRIMARY KEY,
            session_id TEXT,
            forward_rules TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(phone_number, session_id, forward_rules):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (phone_number, session_id, forward_rules) VALUES (%s, %s, %s)",
                   (phone_number, session_id, forward_rules))
    conn.commit()
    conn.close()

def get_user(phone_number):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, forward_rules FROM users WHERE phone_number = %s", (phone_number,))
    result = cursor.fetchone()
    conn.close()
    return result