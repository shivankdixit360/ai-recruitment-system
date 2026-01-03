import streamlit as st
import sqlite3

from tracker.candidate_tracker import add_or_get_candidate
from tracker.submission_tracker import (
    create_job,
    submit_candidate,
    get_candidate_history
)
from tracker.candidate_fetcher import fetch_candidates_for_job
from core.client_aware_ranking import rank_candidates_for_client

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Recruitment System",
    layout="centered"
)

st.title("🤖 AI Recruitment System (MVP)")

# -----------------------------
# Apply DB Schema (safe)
# -----------------------------
conn = sqlite3.connect("database/db.sqlite3")
cursor = conn.cursor()

with open("database/schema.sql", "r") as f:
    schema = f.read()

cursor.executescript(schema)
conn.commit()
conn.close()

# =============================
# 1️⃣ Candidate Section
# =============================
st.header("1️⃣ Add / Get Candidate")

name = st.text_input("Candidate Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
resume_hash = st.text_input("Resume Hash (unique id)")

if st.button("Save Candidate"):
    if name and resume_hash:
        candidate_id = add_or_get_candidate(
            name=name,
            email=email,
            phone=phone,
            resume_hash=resume_hash
        )
        st.success(f"Candidate ID: {candidate_id}")
    else:
        st.warning("Name and Resume Hash required")

# =============================
# 2️⃣ Job Section
# =============================
st.header("2️⃣ Create Job")

job_title = st.text_input("Job Title")
client_name = st.text_input("Client Name")

if st.button("Create Job"):
    if job_title and client_name:
        job_id = create_job(job_title, client_name)
        st.success(f"Job ID: {job_id}")
    else:
        st.warning("Job title and client name required")

# =============================
# 3️⃣ Submission Section
# =============================
st.header("3️⃣ Submit Candidate to Job")

candidate_id_input = st.number_input(
    "Candidate ID", step=1, min_value=1
)
job_id_input = st.number_input(
    "Job ID", step=1, min_value=1
)

if st.button("Submit Candidate"):
    submit_candidate(candidate_id_input, job_id_input)
    st.info("Submission processed (check warning if duplicate)")

# =============================
# 4️⃣ Candidate History
# =============================
st.header("4️⃣ Candidate Submission History")

history_candidate_id = st.number_input(
    "Candidate ID for History", step=1, min_value=1
)

if st.button("Show History"):
    history = get_candidate_history(history_candidate_id)

    if history:
        for h in history:
            st.write(
                f"🧾 Job: {h[0]} | Client: {h[1]} | "
                f"Status: {h[2]} | Date: {h[3]}"
            )
    else:
        st.info("No history found")

# =============================
# 5️⃣ Client Aware Ranking (REAL DATA)
# =============================
st.header("5️⃣ Client Aware Candidate Ranking")

rank_client_name = st.text_input(
    "Client Name for Ranking (same as job client)"
)
rank_job_id = st.number_input(
    "Job ID for Ranking", step=1, min_value=1
)

if st.button("Show Top Candidates for Client"):
    real_candidates = fetch_candidates_for_job(rank_job_id)

    if not real_candidates:
        st.warning("No candidates found for this job")
    else:
        ranked = rank_candidates_for_client(
            client_name=rank_client_name,
            candidates=real_candidates
        )

        st.subheader("🏆 Ranked Candidates")
        for idx, r in enumerate(ranked, start=1):
            st.write(
                f"#{idx} {r['name']} | "
                f"Base Score: {r['base_score']} | "
                f"Final Score: {r['final_score']} | "
                f"Skills: {', '.join(r['skills'])}"
            )
