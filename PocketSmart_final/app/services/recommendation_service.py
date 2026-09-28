from .gemini_service import GeminiService

_ai = GeminiService()

def generate_home(data):
    return _ai.generate("home", data)

def generate_party(data):
    return _ai.generate("party", data)

def generate_jewelry(data, image_bytes=None, mime_type=None):
    return _ai.generate("jewelry", data, image_bytes, mime_type)
