import json
from fastapi import APIRouter, Request
from ..database import get_conn
from ..models.schemas import PartyRequest, PlannerResponse
from ..services.recommendation_service import generate_party
from ..utils.security import get_current_user

router = APIRouter(tags=["Party Planner"])

def save_history(user_id, planner, request_data, response_data):
    with get_conn() as conn:
        conn.execute("INSERT INTO recommendations(user_id,planner_type,request_json,response_json) VALUES(?,?,?,?)",
                     (user_id, planner, json.dumps(request_data, default=str), json.dumps(response_data, default=str)))

@router.post("/generate-party", response_model=PlannerResponse)
def generate(payload: PartyRequest, request: Request):
    user = get_current_user(request)
    result = generate_party(payload)
    save_history(user["id"], "party", payload.model_dump(), result)
    return result
