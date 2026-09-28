from typing import Literal
from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class HomeItem(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    quantity: int = Field(default=1, ge=1, le=50)

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1, max_length=10)
    items: list[HomeItem] = Field(min_length=1, max_length=50)
    style: str = Field(default="modern", min_length=2, max_length=80)
    city: str = Field(default="Mumbai", max_length=80)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=5000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="Flexible", max_length=120)
    city: str = Field(default="Mumbai", max_length=80)
    preferences: str = Field(default="", max_length=1000)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="versatile", max_length=80)
    city: str = Field(default="Mumbai", max_length=80)
    metal: str = Field(default="Any", max_length=50)
    outfit_notes: str = Field(default="", max_length=1000)

class Recommendation(BaseModel):
    category: str
    title: str
    platform: str
    estimated_price: float
    quantity: int = Field(default=1, ge=1)
    rationale: str
    search_url: str

class PlannerResponse(BaseModel):
    planner: Literal["home", "party", "jewelry"]
    budget: float
    total_estimate: float
    budget_remaining: float
    source: Literal["gemini", "fallback"]
    summary: str
    allocations: dict[str, float] = Field(default_factory=dict)
    recommendations: list[Recommendation]
