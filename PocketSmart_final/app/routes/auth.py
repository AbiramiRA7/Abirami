from fastapi import APIRouter, HTTPException, Request, Response
from ..models.schemas import LoginRequest, RegisterRequest, TokenResponse
from ..services.auth_service import authenticate, create_user
from ..utils.security import create_access_token, get_current_user
from ..database import get_conn

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest):
    with get_conn() as conn:
        if conn.execute("SELECT id FROM users WHERE email=?", (payload.email.lower(),)).fetchone():
            raise HTTPException(409, "Email already registered")
    user_id = create_user(payload.name, payload.email, payload.password)
    return {"access_token": create_access_token(user_id), "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, response: Response):
    user = authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(401, "Invalid email or password")
    token = create_access_token(user["id"])
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=60 * 120)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/token", response_model=TokenResponse)
def refresh_token(request: Request):
    user = get_current_user(request)
    return {"access_token": create_access_token(user["id"]), "token_type": "bearer"}
