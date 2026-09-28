from urllib.parse import quote_plus

PLATFORMS = {
    "home": ["Amazon", "Flipkart", "IKEA"],
    "party": ["Swiggy", "Zomato", "OYO", "Amazon"],
    "jewelry": ["Amazon", "Flipkart"],
}

BASE_URLS = {
    "Amazon": "https://www.amazon.in/s?k={q}",
    "Flipkart": "https://www.flipkart.com/search?q={q}",
    "IKEA": "https://www.ikea.com/in/en/search/?q={q}",
    "Swiggy": "https://www.swiggy.com/search?query={q}",
    "Zomato": "https://www.zomato.com/search?query={q}",
    "OYO": "https://www.oyorooms.com/search?location={q}",
}

def search_url(platform: str, query: str, city: str = "") -> str:
    encoded = quote_plus(f"{query} {city}".strip())
    return BASE_URLS.get(platform, "#").format(q=encoded)
