from core.client_preference_adjuster import adjust_score_for_client


def rank_candidates_for_client(client_name, candidates):
    """
    candidates = list of dicts
    Example:
    [
        {"name": "A", "skills": ["SQL", "Power BI"], "base_score": 75},
        {"name": "B", "skills": ["SQL", "Python"], "base_score": 78}
    ]
    """

    ranked = []

    for c in candidates:
        adjusted_score = adjust_score_for_client(
            client_name=client_name,
            candidate_skills=c["skills"],
            base_score=c["base_score"]
        )

        ranked.append({
            "name": c["name"],
            "base_score": c["base_score"],
            "final_score": adjusted_score,
            "skills": c["skills"]
        })

    # sort by final_score (high to low)
    ranked.sort(key=lambda x: x["final_score"], reverse=True)

    return ranked
