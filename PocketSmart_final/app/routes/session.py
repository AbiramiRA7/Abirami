from fastapi import APIRouter, Request
from ..database import get_conn
from ..utils.security import get_current_user

router = APIRouter(tags=["Session"])

@router.get("/session-info")
def session_info(request: Request):
    user = get_current_user(request)
    return {"logged_in": True, "user": {"id": user["id"], "name": user["name"], "email": user["email"]}}

@router.get("/session-data")
def session_data(request: Request):
    user = get_current_user(request)
    with get_conn() as conn:
        rows = conn.execute("SELECT planner_type,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC LIMIT 10", (user["id"],)).fetchall()
    return {"user_id": user["id"], "recent_activity": [dict(row) for row in rows]}
