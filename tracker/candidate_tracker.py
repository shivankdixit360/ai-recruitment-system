import sqlite3
from datetime import datetime

DB_PATH = "database/db.sqlite3"

def add_or_get_candidate(name, email, phone, resume_hash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # check duplicate resume
    cursor.execute(
        "SELECT id FROM candidates WHERE resume_hash = ?",
        (resume_hash,)
    )
    result = cursor.fetchone()

    if result:
        conn.close()
        return result[0]   # candidate already exists

    # add new candidate
    cursor.execute(
        """
        INSERT INTO candidates (name, email, phone, resume_hash, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, phone, resume_hash, datetime.now().isoformat())
    )

    conn.commit()
    candidate_id = cursor.lastrowid
    conn.close()

    return candidate_id
