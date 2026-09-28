from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..utils.security import get_optional_user

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(tags=["Pages"])

def render(request: Request, template: str, **context):
    return templates.TemplateResponse(template, {"request": request, "user": get_optional_user(request), **context})

@router.get("/", response_class=HTMLResponse)
def home(request: Request): return render(request, "home.html")
@router.get("/login", response_class=HTMLResponse)
def login(request: Request): return render(request, "login.html")
@router.get("/register", response_class=HTMLResponse)
def register(request: Request): return render(request, "register.html")
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request): return render(request, "dashboard.html")
@router.get("/history", response_class=HTMLResponse)
def history(request: Request): return render(request, "history.html")
@router.get("/testimonials", response_class=HTMLResponse)
def testimonials(request: Request): return render(request, "testimonials.html")
@router.get("/planner/home", response_class=HTMLResponse)
def home_planner(request: Request): return render(request, "planners/home_planner.html")
@router.get("/planner/party", response_class=HTMLResponse)
def party_planner(request: Request): return render(request, "planners/party_planner.html")
@router.get("/planner/jewelry", response_class=HTMLResponse)
def jewelry_planner(request: Request): return render(request, "planners/jewelry_planner.html")
