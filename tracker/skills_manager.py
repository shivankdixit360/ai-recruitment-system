import sqlite3

DB_PATH = "database/db.sqlite3"

def save_candidate_skills(candidate_id, skills):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # clean old skills (re-save scenario)
    cursor.execute(
        "DELETE FROM candidate_skills WHERE candidate_id = ?",
        (candidate_id,)
    )

    for skill in skills:
        cursor.execute(
            """
            INSERT INTO candidate_skills (candidate_id, skill)
            VALUES (?, ?)
            """,
            (candidate_id, skill)
        )

    conn.commit()
    conn.close()


def get_candidate_skills(candidate_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT skill FROM candidate_skills
        WHERE candidate_id = ?
        """,
        (candidate_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [r[0] for r in rows]

