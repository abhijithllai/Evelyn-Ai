import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Gemini API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def rephrase_as_evelyn(response):
    """
    Transforms a response into Evelyn’s signature style:
    - Simple, elegant, and emotionally warm.
    - Clear language, easy for anyone to understand.
    - 2–3 sentences per paragraph.
    - Adds TWO empty lines between each paragraph.
    - Max 4–5 paragraphs to avoid long responses.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f"""
You are Evelyn, a lovely, intelligent AI assistant with a warm and simple style.

Rewrite the following message to match your voice:
- Use clear, simple language that anyone can understand.
- Keep the tone elegant, kind, and softly emotional.
- Keep each paragraph short (2–3 sentences max).
- Add TWO empty lines between each paragraph.
- Limit the total response to 4–5 short paragraphs only.

Original Content:
\"\"\"{response}\"\"\" 

Evelyn's Final Response:
"""

        response_obj = model.generate_content(prompt)

        if response_obj and hasattr(response_obj, "text") and response_obj.text.strip():
            return response_obj.text.strip()

        print("❌ Gemini refused to rephrase. Using fallback.")
        return response

    except Exception as e:
        print(f"❌ Error with Gemini API: {e}")
        return response
