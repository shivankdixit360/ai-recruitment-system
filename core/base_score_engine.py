def calculate_base_score(jd_skills, candidate_skills):
    """
    jd_skills: list -> ["SQL", "Power BI", "Python"]
    candidate_skills: list -> ["SQL", "Power BI"]
    """

    if not jd_skills:
        return 0

    matched = 0

    for skill in jd_skills:
        if skill in candidate_skills:
            matched += 1

    score = (matched / len(jd_skills)) * 100
    return round(score)
