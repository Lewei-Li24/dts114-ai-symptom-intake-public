DROP TABLE IF EXISTS symptom_summaries;
DROP TABLE IF EXISTS followup_questions;
DROP TABLE IF EXISTS symptom_inputs;
DROP TABLE IF EXISTS user_sessions;
DROP TABLE IF EXISTS health_records;
DROP TABLE IF EXISTS user_profiles;

CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_name TEXT,
    age INTEGER,
    sex TEXT,
    height_cm REAL,
    weight_kg REAL,
    allergies TEXT,
    current_medications TEXT,
    chronic_conditions TEXT,
    past_history TEXT,
    family_history TEXT,
    emergency_contact TEXT,
    consent_use_history INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL DEFAULT 1,
    record_type TEXT NOT NULL DEFAULT 'checkup',
    title TEXT NOT NULL,
    record_date TEXT,
    source_text TEXT,
    structured_content TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES user_profiles (id)
);

CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    user_label TEXT NOT NULL DEFAULT 'anonymous-user',
    triage_level TEXT NOT NULL DEFAULT 'pending',
    safety_triggered INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES user_profiles (id)
);

CREATE TABLE symptom_inputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    primary_symptom TEXT NOT NULL,
    duration TEXT NOT NULL,
    severity INTEGER NOT NULL,
    additional_context TEXT,
    red_flags TEXT NOT NULL DEFAULT '[]',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions (id)
);

CREATE TABLE followup_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    answer_text TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions (id)
);

CREATE TABLE symptom_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    main_complaint TEXT NOT NULL,
    structured_summary TEXT NOT NULL,
    triage_level TEXT NOT NULL,
    next_steps TEXT NOT NULL,
    disclaimer TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions (id)
);
