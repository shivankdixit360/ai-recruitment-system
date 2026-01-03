import sqlite3

from tracker.skills_manager import get_candidate_skills
from tracker.jd_skills_manager import get_job_skills
from core.base_score_engine import calculate_base_score

DB_PATH = "database/db.sqlite3"

def fetch_candidates_for_job(job_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.id, c.name
        FROM submissions s
        JOIN candidates c ON s.candidate_id = c.id
        WHERE s.job_id = ?
        """,
        (job_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    jd_skills = get_job_skills(job_id)

    candidates = []

    for cid, name in rows:
        candidate_skills = get_candidate_skills(cid)

        base_score = calculate_base_score(
            jd_skills=jd_skills,
            candidate_skills=candidate_skills
        )

        candidates.append({
            "name": name,
            "skills": candidate_skills,
            "base_score": base_score
        })

    return candidates
