"""
app/database.py
All database helper functions using context manager for safe connection handling.
"""
import sqlite3
import json
import os
import logging
from contextlib import contextmanager
from typing import Optional, List, Dict

log = logging.getLogger(__name__)
DB_PATH = os.getenv("DB_PATH", "college_chatbot.db")


@contextmanager
def get_db():
    """Open DB connection, commit on success, rollback on error, always close."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# --- Intents ---

def get_all_intents() -> List[Dict]:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM intents").fetchall()
        return [
            {
                "id": r["id"],
                "tag": r["tag"],
                "mode": r["mode"],
                "patterns": json.loads(r["patterns"]),
                "responses": json.loads(r["responses"]),
                "context": r["context"] or ""
            }
            for r in rows
        ]


# --- Conversations ---

def save_conversation(user_id: str, mode: str, user_message: str,
                      bot_response: str, intent_tag: Optional[str], confidence: float):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO conversations (user_id,mode,user_message,bot_response,intent_tag,confidence) VALUES (?,?,?,?,?,?)",
            (user_id, mode, user_message, bot_response, intent_tag, confidence)
        )


def get_conversation_history(user_id: str, limit: int = 20) -> List[Dict]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT user_message, bot_response, intent_tag, confidence, mode, timestamp FROM conversations WHERE user_id=? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
        return [dict(r) for r in reversed(rows)]


def clear_conversation_history(user_id: str):
    with get_db() as conn:
        conn.execute("DELETE FROM conversations WHERE user_id=?", (user_id,))


# --- Subjects ---

def get_subjects(department: str = "CSE", semester: Optional[int] = None) -> List[Dict]:
    with get_db() as conn:
        if semester:
            rows = conn.execute(
                "SELECT * FROM subjects WHERE department=? AND semester=? ORDER BY type, code",
                (department.upper(), semester)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM subjects WHERE department=? ORDER BY semester, type, code",
                (department.upper(),)
            ).fetchall()
        return [dict(r) for r in rows]


def search_subjects(keyword: str) -> List[Dict]:
    kw = f"%{keyword}%"
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM subjects WHERE name LIKE ? OR code LIKE ? OR description LIKE ?",
            (kw, kw, kw)
        ).fetchall()
        return [dict(r) for r in rows]


# --- Syllabus ---

def get_syllabus(subject_code: str) -> List[Dict]:
    with get_db() as conn:
        rows = conn.execute(
            """SELECT s.*, sub.name as subject_name, sub.credits
               FROM syllabus s
               JOIN subjects sub ON sub.code = s.subject_code
               WHERE s.subject_code=?
               ORDER BY s.unit_number""",
            (subject_code.upper(),)
        ).fetchall()
        return [dict(r) for r in rows]


def search_syllabus_by_name(name_keyword: str) -> List[Dict]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT code FROM subjects WHERE name LIKE ? LIMIT 1",
            (f"%{name_keyword}%",)
        ).fetchone()
        if not row:
            return []
        return get_syllabus(row["code"])


# --- Timetable ---

def get_timetable(department: str, semester: int, day: Optional[str] = None) -> List[Dict]:
    with get_db() as conn:
        if day:
            rows = conn.execute(
                "SELECT * FROM timetable WHERE department=? AND semester=? AND day=? ORDER BY period",
                (department.upper(), semester, day.capitalize())
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM timetable WHERE department=? AND semester=? ORDER BY day, period",
                (department.upper(), semester)
            ).fetchall()
        return [dict(r) for r in rows]


def find_subject_in_timetable(subject_keyword: str, department: str = "CSE", semester: int = 3) -> List[Dict]:
    kw = f"%{subject_keyword}%"
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM timetable WHERE department=? AND semester=? AND (subject_name LIKE ? OR subject_code LIKE ?) ORDER BY day, period",
            (department.upper(), semester, kw, kw)
        ).fetchall()
        return [dict(r) for r in rows]


# --- Admission data ---

def get_programs(department: Optional[str] = None) -> List[Dict]:
    with get_db() as conn:
        if department:
            rows = conn.execute("SELECT * FROM programs WHERE department=?", (department.upper(),)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM programs ORDER BY degree, name").fetchall()
        return [dict(r) for r in rows]


def get_placement_info() -> List[Dict]:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM placements ORDER BY year DESC").fetchall()
        return [dict(r) for r in rows]


def get_admission_dates() -> List[Dict]:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM admission_dates ORDER BY start_date").fetchall()
        return [dict(r) for r in rows]


def get_college_info() -> Dict:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM colleges LIMIT 1").fetchone()
        return dict(row) if row else {}


def get_facilities() -> List[Dict]:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM facilities ORDER BY name").fetchall()
        return [dict(r) for r in rows]
