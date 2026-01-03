import sqlite3

DB_PATH = "database/db.sqlite3"

# simple rules (easy to change later)
BONUS_POINTS = 5
PENALTY_POINTS = -3


def adjust_score_for_client(client_name, candidate_skills, base_score):
    """
    candidate_skills: list of skills like ["SQL", "Power BI"]
    base_score: int (0–100)
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT skill, decision
        FROM client_memory
        WHERE client_name = ?
        """,
        (client_name,)
    )

    memory_rows = cursor.fetchall()
    conn.close()

    final_score = base_score

    for skill, decision in memory_rows:
        if skill in candidate_skills:
            if decision == "Accepted":
                final_score += BONUS_POINTS
            elif decision == "Rejected":
                final_score += PENALTY_POINTS

    # safety guard
    if final_score > 100:
        final_score = 100
    if final_score < 0:
        final_score = 0

    return final_score
