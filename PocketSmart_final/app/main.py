from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import init_db
from .routes import auth, pages, home, party, jewelry, recommendations, session

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(pages.router)
app.include_router(auth.router, prefix="/api")
app.include_router(home.router, prefix="/api")
app.include_router(party.router, prefix="/api")
app.include_router(jewelry.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(session.router, prefix="/api")

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": settings.app_name}

@app.get("/startup", tags=["System"])
def startup():
    return {"status": "ready", "gemini_configured": bool(settings.gemini_api_key), "model": settings.gemini_model}
