import os
from google import genai
from google.genai import types
from src.schema import SupportTicketExtracted


def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Не знайдено GEMINI_API_KEY. Перевірте файл .env у корені проєкту.")

    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=60_000,  # 60 секунд
            retry_options=types.HttpRetryOptions(
                attempts=6,
                initial_delay=2.0,
                max_delay=30.0,
                http_status_codes=[408, 429, 500, 502, 503, 504],
            ),
        ),
    )


def extract_ticket(
    client: genai.Client,
    system_prompt: str,
    raw_text: str,
    model: str = "gemini-3.8-flash",
) -> dict:
    response = client.models.generate_content(
        model=model,
        contents=raw_text,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=SupportTicketExtracted,
            temperature=0.0,
        ),
    )
    if response.parsed is None:
        raise ValueError(f"Модель не повернула валідний об'єкт: {response.text}")
    return response.parsed.model_dump()