from fastapi import APIRouter, HTTPException, Header
from app.database_sqlite import Database
from pydantic import BaseModel
import base64
 
router = APIRouter()
 
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "stlourdes2024"
 
class LoginRequest(BaseModel):
    username: str
    password: str
 
def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        decoded = base64.b64decode(authorization[6:]).decode("utf-8")
        user, pwd = decoded.split(":", 1)
        if user != ADMIN_USERNAME or pwd != ADMIN_PASSWORD:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
 
@router.post("/login")
def login(req: LoginRequest):
    """JSON login — no browser Basic Auth popup"""
    if req.username != ADMIN_USERNAME or req.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = base64.b64encode(f"{req.username}:{req.password}".encode()).decode()
    return {"status": "ok", "token": token}
 
@router.get("/stats")
def get_stats(authorization: str = Header(None)):
    verify_token(authorization)
    total      = Database.execute_query("SELECT COUNT(*) as c FROM conversations")[0]["c"]
    today      = Database.execute_query("SELECT COUNT(*) as c FROM conversations WHERE DATE(created_at) = DATE('now')")[0]["c"]
    users      = Database.execute_query("SELECT COUNT(DISTINCT user_id) as c FROM conversations")[0]["c"]
    unanswered = Database.execute_query("SELECT COUNT(*) as c FROM conversations WHERE intent IN ('unknown','academic_unknown')")[0]["c"]
 
    academic_intents = (
        "'syllabus_cse','syllabus_it','syllabus_aids','syllabus_cyber','syllabus_mech','syllabus_general',"
        "'notes_general','notes_cse','notes_it','notes_aids','notes_cyber','notes_mech',"
        "'timetable_general','timetable_cse','timetable_it','timetable_aids','timetable_cyber','timetable_mech',"
        "'exam_schedule','internal_exam','exam_results','exam_pattern',"
        "'faculty_general','faculty_cse','faculty_it','faculty_aids','faculty_cyber','faculty_mech',"
        "'academic_calendar','attendance','library_academic','lab_sessions','project','internship',"
        "'download_ds','download_cn','download_dbms','download_os','download_ml','download_math',"
        "'academic_greeting','academic_unknown'"
    )
    academic  = Database.execute_query(f"SELECT COUNT(*) as c FROM conversations WHERE intent IN ({academic_intents})")[0]["c"]
    admission = total - academic
 
    avg_row  = Database.execute_query("SELECT ROUND(AVG(confidence)*100,1) as c FROM conversations WHERE confidence IS NOT NULL")
    avg_conf = avg_row[0]["c"] if avg_row else 0
 
    return {
        "total_conversations": total,
        "today_conversations": today,
        "unique_users": users,
        "unanswered_queries": unanswered,
        "admission_queries": admission,
        "academic_queries": academic,
        "avg_confidence": avg_conf,
    }
 
@router.get("/top-intents")
def get_top_intents(limit: int = 10, authorization: str = Header(None)):
    verify_token(authorization)
    rows = Database.execute_query(f"""
        SELECT intent, COUNT(*) as count, ROUND(AVG(confidence)*100,1) as avg_conf
        FROM conversations WHERE intent IS NOT NULL AND intent != ''
        GROUP BY intent ORDER BY count DESC LIMIT {limit}
    """)
    return [{"intent": r["intent"], "count": r["count"], "avg_conf": r["avg_conf"]} for r in rows]
 
@router.get("/daily-activity")
def get_daily_activity(days: int = 14, authorization: str = Header(None)):
    verify_token(authorization)
    rows = Database.execute_query(f"""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM conversations WHERE created_at >= DATE('now', '-{days} days')
        GROUP BY DATE(created_at) ORDER BY date ASC
    """)
    return [{"date": r["date"], "count": r["count"]} for r in rows]
 
@router.get("/hourly-activity")
def get_hourly_activity(authorization: str = Header(None)):
    verify_token(authorization)
    rows = Database.execute_query("""
        SELECT CAST(strftime('%H', created_at) AS INTEGER) as hour, COUNT(*) as count
        FROM conversations GROUP BY hour ORDER BY hour ASC
    """)
    hour_map = {r["hour"]: r["count"] for r in rows}
    return [{"hour": h, "count": hour_map.get(h, 0)} for h in range(24)]
 
@router.get("/unanswered")
def get_unanswered(limit: int = 20, authorization: str = Header(None)):
    verify_token(authorization)
    rows = Database.execute_query(f"""
        SELECT message, created_at, user_id FROM conversations
        WHERE intent IN ('unknown','academic_unknown')
        ORDER BY created_at DESC LIMIT {limit}
    """)
    return [{"message": r["message"], "time": r["created_at"], "user": r["user_id"]} for r in rows]
 
@router.get("/recent-conversations")
def get_recent(limit: int = 30, authorization: str = Header(None)):
    verify_token(authorization)
    rows = Database.execute_query(f"""
        SELECT user_id, message, intent, confidence, created_at
        FROM conversations ORDER BY created_at DESC LIMIT {limit}
    """)
    return [{
        "user": r["user_id"], "message": r["message"], "intent": r["intent"],
        "confidence": round((r["confidence"] or 0) * 100, 1), "time": r["created_at"],
    } for r in rows]
 
@router.get("/mode-split")
def get_mode_split(authorization: str = Header(None)):
    verify_token(authorization)
    academic_intents = (
        "'syllabus_cse','syllabus_it','syllabus_aids','syllabus_cyber','syllabus_mech','syllabus_general',"
        "'timetable_cse','timetable_it','timetable_aids','timetable_cyber','timetable_mech','timetable_general',"
        "'download_ds','download_cn','download_dbms','download_os','download_ml','download_math',"
        "'academic_greeting','academic_unknown'"
    )
    academic  = Database.execute_query(f"SELECT COUNT(*) as c FROM conversations WHERE intent IN ({academic_intents})")[0]["c"]
    total     = Database.execute_query("SELECT COUNT(*) as c FROM conversations")[0]["c"]
    return {"admission": total - academic, "academic": academic, "total": total}