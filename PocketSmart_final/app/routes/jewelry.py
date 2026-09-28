import json
from fastapi import APIRouter, File, Form, Request, UploadFile
from ..database import get_conn
from ..models.schemas import JewelryRequest, PlannerResponse
from ..services.recommendation_service import generate_jewelry
from ..utils.security import get_current_user
from ..utils.validators import read_optional_image

router = APIRouter(tags=["Jewelry Planner"])

def save_history(user_id, payload, response_data):
    with get_conn() as conn:
        conn.execute("INSERT INTO recommendations(user_id,planner_type,request_json,response_json) VALUES(?,?,?,?)",
                     (user_id, "jewelry", json.dumps(payload, default=str), json.dumps(response_data, default=str)))

@router.post("/generate-jewelry", response_model=PlannerResponse)
async def generate(request: Request, budget: float = Form(...), occasion: str = Form(...), style: str = Form("versatile"),
                   city: str = Form("Mumbai"), metal: str = Form("Any"), outfit_notes: str = Form(""),
                   outfit: UploadFile | None = File(None)):
    user = get_current_user(request)
    payload = JewelryRequest(budget=budget, occasion=occasion, style=style, city=city, metal=metal, outfit_notes=outfit_notes)
    image_bytes, mime_type = await read_optional_image(outfit)
    result = generate_jewelry(payload, image_bytes, mime_type)
    save_history(user["id"], payload.model_dump(), result)
    return result
