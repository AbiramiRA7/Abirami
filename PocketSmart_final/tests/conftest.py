import os
from pathlib import Path

TEST_DB = Path(__file__).resolve().parent / "test_pocketsmart.db"
if TEST_DB.exists(): TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["GEMINI_API_KEY"] = ""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

@pytest.fixture(scope="session", autouse=True)
def database():
    init_db()
    yield
    if TEST_DB.exists(): TEST_DB.unlink()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def registered_user(client):
    email = "test@example.com"
    response = client.post("/api/register", json={"name":"Test User","email":email,"password":"password123"})
    assert response.status_code == 200
    return {"email": email, "password":"password123", "token": response.json()["access_token"]}
