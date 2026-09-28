import json

def to_json(value) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)

def total_cost(recommendations: list[dict]) -> float:
    return round(sum(float(r.get("estimated_price", 0)) * int(r.get("quantity", 1)) for r in recommendations), 2)
