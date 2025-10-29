import sqlite3
import os

# Define database path once to avoid mismatches
DB_PATH = os.path.join("database", "resume_data.db")

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            skills TEXT,
            experience TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Convert lists to strings
    skills = ", ".join(data["skills"]) if isinstance(data["skills"], list) else data["skills"]
    experience = "\n".join(data["experience"]) if isinstance(data["experience"], list) else data["experience"]

    c.execute('''
        INSERT INTO resumes (name, email, skills, experience)
        VALUES (?, ?, ?, ?)
    ''', (data["name"], data["email"], skills, experience))

    conn.commit()
    conn.close()
