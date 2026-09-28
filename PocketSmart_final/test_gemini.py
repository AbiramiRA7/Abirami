from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API key loaded:", bool(api_key))

if not api_key:
    raise RuntimeError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)

try:
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="Reply with exactly: PocketSmart AI works!"
    )

    print("\nSUCCESS!")
    print(interaction.output_text)

except Exception as e:
    print("\nGEMINI ERROR:")
    print(type(e).__name__)
    print(str(e))