import json
from fastapi import APIRouter, HTTPException, Request
from ..database import get_conn
from ..utils.security import get_current_user

router = APIRouter(tags=["Recommendations"])

@router.get("/history")
def history(request: Request):
    user = get_current_user(request)
    with get_conn() as conn:
        rows = conn.execute("SELECT id,planner_type,request_json,response_json,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC", (user["id"],)).fetchall()
    return [{"id": r["id"], "planner": r["planner_type"], "request": json.loads(r["request_json"]),
             "response": json.loads(r["response_json"]), "created_at": r["created_at"]} for r in rows]

@router.get("/recommendations-details/{recommendation_id}")
def details(recommendation_id: int, request: Request):
    user = get_current_user(request)
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM recommendations WHERE id=? AND user_id=?", (recommendation_id, user["id"])).fetchone()
    if not row:
        raise HTTPException(404, "Recommendation not found")
    return {"id": row["id"], "planner": row["planner_type"], "request": json.loads(row["request_json"]),
            "response": json.loads(row["response_json"]), "created_at": row["created_at"]}
