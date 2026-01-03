import sqlite3

DB_PATH = "database/db.sqlite3"

def save_job_skills(job_id, skills):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # overwrite old JD skills
    cursor.execute(
        "DELETE FROM job_skills WHERE job_id = ?",
        (job_id,)
    )

    for skill in skills:
        cursor.execute(
            """
            INSERT INTO job_skills (job_id, skill)
            VALUES (?, ?)
            """,
            (job_id, skill)
        )

    conn.commit()
    conn.close()


def get_job_skills(job_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT skill FROM job_skills
        WHERE job_id = ?
        """,
        (job_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [r[0] for r in rows]
