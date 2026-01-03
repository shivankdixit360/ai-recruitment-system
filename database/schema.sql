CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    resume_hash TEXT UNIQUE,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT,
    client_name TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    job_id INTEGER,
    status TEXT,
    submitted_at TEXT,
    recruiter_note TEXT,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id),
    FOREIGN KEY(job_id) REFERENCES jobs(id)
);


CREATE TABLE IF NOT EXISTS client_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT,
    skill TEXT,
    decision TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS candidate_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    skill TEXT,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
);

CREATE TABLE IF NOT EXISTS job_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    skill TEXT,
    FOREIGN KEY(job_id) REFERENCES jobs(id)
);



