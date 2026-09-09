from google import genai

from app.core.config import settings


class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        

    def generate_summary(self, text: str) -> str:
        prompt = f"""
You are an AI assistant that summarizes PDF documents.

Read the document content below and provide a concise summary
in exactly 3 to 5 sentences.

Focus on:
- the main topic
- important findings or information
- key conclusions
- important details that a reader should know

Do not use bullet points.
Do not mention that you are an AI.
Do not invent information.

DOCUMENT:
{text}
"""

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return response.text.strip()

    def generate_text(self, prompt: str) -> str:
        """
        Generate a text response using Gemini.
        """

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        return response.text.strip()