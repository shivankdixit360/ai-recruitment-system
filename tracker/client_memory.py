import sqlite3
from datetime import datetime

DB_PATH = "database/db.sqlite3"


def save_client_memory(client_name, skill, decision):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO client_memory (client_name, skill, decision, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (client_name, skill, decision, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()

def get_client_preferences(client_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT skill, decision, COUNT(*) as count
        FROM client_memory
        WHERE client_name = ?
        GROUP BY skill, decision
        ORDER BY count DESC
        """,
        (client_name,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows

