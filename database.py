"""
Database Layer for IBM Granite Interview Trainer Agent
Persistent SQLite storage with IBM Cloudant adapter compatibility.
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.config import settings

def get_connection():
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Candidates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        experience_level TEXT,
        education TEXT,
        college TEXT,
        target_role TEXT,
        industry TEXT,
        technical_skills TEXT,
        programming_languages TEXT,
        preferred_company TEXT,
        interview_type TEXT,
        difficulty TEXT,
        additional_requirements TEXT,
        resume_filename TEXT,
        resume_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Resume analysis table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_email TEXT,
        extracted_skills TEXT,
        missing_skills TEXT,
        detected_keywords TEXT,
        education_summary TEXT,
        experience_summary TEXT,
        projects_summary TEXT,
        profile_readiness_score INTEGER,
        docling_pages_parsed INTEGER,
        docling_elements_count INTEGER,
        recommendations TEXT,
        docling_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Mock interview sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mock_sessions (
        id TEXT PRIMARY KEY,
        candidate_email TEXT,
        job_role TEXT,
        interview_type TEXT,
        difficulty TEXT,
        total_questions INTEGER,
        completed_questions INTEGER DEFAULT 0,
        average_score REAL DEFAULT 0,
        status TEXT DEFAULT 'in_progress', -- in_progress, completed
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    )
    """)

    # Mock interview questions & candidate answers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mock_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        question_id TEXT,
        question_text TEXT,
        category TEXT,
        difficulty TEXT,
        user_answer TEXT,
        evaluation_json TEXT,
        score INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Practiced question bank / history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_email TEXT,
        question TEXT,
        category TEXT,
        difficulty TEXT,
        model_answer TEXT,
        user_answer TEXT,
        score INTEGER,
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Saved Roadmaps
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_email TEXT,
        target_role TEXT,
        roadmap_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Knowledge Base Documents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_documents (
        id TEXT PRIMARY KEY,
        title TEXT,
        category TEXT,
        source TEXT,
        content TEXT,
        chunk_count INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Seed default sample candidate if empty
    cursor.execute("SELECT COUNT(*) FROM candidates")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO candidates (
            name, email, password, experience_level, education, college, target_role,
            industry, technical_skills, programming_languages, preferred_company,
            interview_type, difficulty, additional_requirements
        ) VALUES (
            'Alex Chen', 'alex.chen@skillsbuild.ibm.edu', 'ibm2026', 'Fresher',
            'B.Tech Computer Science and Engineering', 'IBM SkillsBuild University Partner College',
            'Cloud Application Developer', 'Cloud Computing & Enterprise Software',
            '["Python", "Cloud Fundamentals", "REST APIs", "SQL", "Git", "Docker Basics"]',
            '["Python", "SQL", "Java"]', 'IBM', 'Mixed', 'Intermediate',
            'Focus on cloud architecture, API design, and behavioral STAR techniques.'
        )
        """)
        conn.commit()

    conn.close()

# Helper operations
def get_candidate(email: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["technical_skills"] = json.loads(data["technical_skills"]) if data.get("technical_skills") else []
    data["programming_languages"] = json.loads(data["programming_languages"]) if data.get("programming_languages") else []
    return data

def save_or_update_candidate(data: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM candidates WHERE email = ?", (data["email"],))
    row = cursor.fetchone()

    tech_skills = json.dumps(data.get("technical_skills", []))
    prog_langs = json.dumps(data.get("programming_languages", []))

    if row:
        cursor.execute("""
        UPDATE candidates SET
            name = ?, experience_level = ?, education = ?, college = ?,
            target_role = ?, industry = ?, technical_skills = ?,
            programming_languages = ?, preferred_company = ?,
            interview_type = ?, difficulty = ?, additional_requirements = ?,
            resume_filename = coalesce(?, resume_filename),
            resume_text = coalesce(?, resume_text),
            updated_at = CURRENT_TIMESTAMP
        WHERE email = ?
        """, (
            data.get("name"), data.get("experience_level"), data.get("education"),
            data.get("college"), data.get("target_role"), data.get("industry"),
            tech_skills, prog_langs, data.get("preferred_company"),
            data.get("interview_type"), data.get("difficulty"),
            data.get("additional_requirements"), data.get("resume_filename"),
            data.get("resume_text"), data["email"]
        ))
    else:
        cursor.execute("""
        INSERT INTO candidates (
            name, email, password, experience_level, education, college,
            target_role, industry, technical_skills, programming_languages,
            preferred_company, interview_type, difficulty, additional_requirements,
            resume_filename, resume_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("name"), data["email"], data.get("password", "ibm_pass"),
            data.get("experience_level"), data.get("education"), data.get("college"),
            data.get("target_role"), data.get("industry"), tech_skills, prog_langs,
            data.get("preferred_company"), data.get("interview_type"),
            data.get("difficulty"), data.get("additional_requirements"),
            data.get("resume_filename"), data.get("resume_text")
        ))
    conn.commit()
    conn.close()

def save_resume_analysis(email: str, analysis: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO resume_analyses (
        candidate_email, extracted_skills, missing_skills, detected_keywords,
        education_summary, experience_summary, projects_summary,
        profile_readiness_score, docling_pages_parsed, docling_elements_count,
        recommendations, docling_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email,
        json.dumps(analysis.get("extracted_skills", [])),
        json.dumps(analysis.get("missing_skills", [])),
        json.dumps(analysis.get("detected_keywords", [])),
        analysis.get("education_summary", ""),
        analysis.get("experience_summary", ""),
        json.dumps(analysis.get("projects_summary", [])),
        analysis.get("profile_readiness_score", 70),
        analysis.get("docling_pages_parsed", 1),
        analysis.get("docling_elements_count", 0),
        json.dumps(analysis.get("recommendations", [])),
        json.dumps(analysis.get("docling_json", {}))
    ))
    conn.commit()
    conn.close()

def get_latest_resume_analysis(email: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM resume_analyses WHERE candidate_email = ? ORDER BY id DESC LIMIT 1
    """, (email,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    for col in ["extracted_skills", "missing_skills", "detected_keywords", "projects_summary", "recommendations", "docling_json"]:
        if d.get(col):
            try:
                d[col] = json.loads(d[col])
            except Exception:
                pass
    return d

def get_dashboard_metrics(email: str) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()

    # Candidate profile
    cursor.execute("SELECT * FROM candidates WHERE email = ?", (email,))
    cand = cursor.fetchone()

    # Resume analysis
    cursor.execute("SELECT * FROM resume_analyses WHERE candidate_email = ? ORDER BY id DESC LIMIT 1", (email,))
    resume_row = cursor.fetchone()

    # Mock sessions
    cursor.execute("SELECT COUNT(*), AVG(average_score) FROM mock_sessions WHERE candidate_email = ? AND status = 'completed'", (email,))
    mock_stats = cursor.fetchone()
    mocks_completed = mock_stats[0] or 0
    avg_mock_score = round(mock_stats[1] or 0, 1)

    # Questions answered
    cursor.execute("SELECT COUNT(*), AVG(score) FROM mock_answers ma JOIN mock_sessions ms ON ma.session_id = ms.id WHERE ms.candidate_email = ?", (email,))
    q_stats = cursor.fetchone()
    total_q_practiced = q_stats[0] or 0
    avg_q_score = round(q_stats[1] or 0, 1)

    # Combined average score
    overall_avg_score = round((avg_mock_score + avg_q_score) / 2 if (mocks_completed and total_q_practiced) else (avg_mock_score or avg_q_score or 75.0), 1)

    # Skills from profile or resume
    strong_skills = []
    missing_skills = []
    readiness_score = 65

    if resume_row:
        try:
            strong_skills = json.loads(resume_row["extracted_skills"])[:6]
            missing_skills = json.loads(resume_row["missing_skills"])[:5]
            readiness_score = resume_row["profile_readiness_score"]
        except Exception:
            pass
    elif cand and cand["technical_skills"]:
        try:
            strong_skills = json.loads(cand["technical_skills"])[:6]
        except Exception:
            pass

    conn.close()

    # Progress calculation based on practice activity
    progress_percentage = min(100, int((mocks_completed * 20) + (total_q_practiced * 8) + (readiness_score * 0.4)))

    return {
        "candidate_name": cand["name"] if cand else "Candidate",
        "target_role": cand["target_role"] if cand else "Cloud Application Developer",
        "experience_level": cand["experience_level"] if cand else "Fresher",
        "resume_analysis_status": "Analyzed via IBM Docling" if resume_row else "Pending Resume Upload",
        "resume_readiness_score": readiness_score,
        "total_questions_practiced": total_q_practiced,
        "mock_interviews_completed": mocks_completed,
        "average_practice_score": overall_avg_score,
        "strong_skills": strong_skills or ["Python", "SQL", "Cloud Fundamentals", "REST APIs"],
        "improvement_areas": missing_skills or ["Distributed Systems", "Kubernetes", "Behavioral STAR Stories"],
        "preparation_progress": progress_percentage,
        "recommended_activities": [
            {"title": "Take a 5-Question Mixed Mock Interview", "type": "Mock Practice", "badge": "High Priority"},
            {"title": f"Deepen Technical Knowledge in {missing_skills[0] if missing_skills else 'Cloud Architecture'}", "type": "Topic Practice", "badge": "Skill Gap"},
            {"title": "Review Personalized Preparation Roadmap for Day 1", "type": "Roadmap", "badge": "Next Step"}
        ]
    }

# Initialize database on module import
init_db()
