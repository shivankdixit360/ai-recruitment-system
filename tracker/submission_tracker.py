import sqlite3
from datetime import datetime

DB_PATH = "database/db.sqlite3"


def create_job(job_title, client_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs (job_title, client_name, created_at)
        VALUES (?, ?, ?)
        """,
        (job_title, client_name, datetime.now().isoformat())
    )

    conn.commit()
    job_id = cursor.lastrowid
    conn.close()

    return job_id


def check_duplicate_submission(candidate_id, job_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id FROM submissions
        WHERE candidate_id = ? AND job_id = ?
        """,
        (candidate_id, job_id)
    )

    result = cursor.fetchone()
    conn.close()

    return True if result else False


def submit_candidate(candidate_id, job_id, status="Sent"):
    if check_duplicate_submission(candidate_id, job_id):
        print("⚠️ Warning: Candidate already submitted for this job")
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO submissions (candidate_id, job_id, status, submitted_at)
        VALUES (?, ?, ?, ?)
        """,
        (candidate_id, job_id, status, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()

    print("✅ Candidate submitted successfully")


def update_submission_status(submission_id, new_status, note=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE submissions
        SET status = ?, recruiter_note = ?
        WHERE id = ?
        """,
        (new_status, note, submission_id)
    )

    conn.commit()
    conn.close()


def get_candidate_history(candidate_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT jobs.job_title,
               jobs.client_name,
               submissions.status,
               submissions.submitted_at
        FROM submissions
        JOIN jobs ON submissions.job_id = jobs.id
        WHERE submissions.candidate_id = ?
        """,
        (candidate_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows
