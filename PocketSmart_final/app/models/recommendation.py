from dataclasses import dataclass

@dataclass(frozen=True)
class RecommendationRecord:
    id: int
    user_id: int
    planner_type: str
    request_json: str
    response_json: str
    created_at: str
