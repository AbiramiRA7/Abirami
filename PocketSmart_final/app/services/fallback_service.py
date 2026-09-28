from .marketplace_service import PLATFORMS, search_url

def _platform(kind: str, index: int) -> str:
    options = PLATFORMS[kind]
    return options[index % len(options)]

def home_fallback(data):
    item_names = [item.name for item in data.items]
    defaults = item_names or ["Ceiling light", "Ceiling fan", "Dining table", "Wall art"]
    prices = [1500, 3500, 8500, 1800, 6500, 2200]
    recs = []
    for i, name in enumerate(defaults[:8]):
        platform = _platform("home", i)
        price = prices[i % len(prices)]
        recs.append({"category": "Home", "title": name, "platform": platform, "estimated_price": price, "quantity": 1,
                     "rationale": f"Illustrative {data.style} option for the selected rooms.", "search_url": search_url(platform, name, data.city)})
    return recs

def party_fallback(data):
    allocations = [("Catering", .45), ("Venue", .25), ("Decoration", .15), ("Entertainment", .10), ("Contingency", .05)]
    recs = []
    for i, (category, pct) in enumerate(allocations):
        title = f"{category} option for {data.event_type}"
        platform = _platform("party", i)
        recs.append({"category": category, "title": title, "platform": platform,
                     "estimated_price": round(data.budget * pct, 2), "quantity": 1,
                     "rationale": f"Illustrative allocation for {data.guests} guests.",
                     "search_url": search_url(platform, title, data.city)})
    return recs

def jewelry_fallback(data):
    options = [("Earrings", "Statement earrings", 2200), ("Necklace", "Pendant necklace", 3500), ("Bracelet", "Slim bracelet", 1800)]
    recs = []
    for i, (cat, title, price) in enumerate(options):
        platform = _platform("jewelry", i)
        recs.append({"category": cat, "title": title, "platform": platform, "estimated_price": price, "quantity": 1,
                     "rationale": f"A {data.style} suggestion for {data.occasion}.", "search_url": search_url(platform, title, data.city)})
    return recs
