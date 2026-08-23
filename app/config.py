"""
Project Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reads secret API keys from the .env file.
If any required key is missing, the project automatically
falls back to "mock mode" (simulated AI responses, no real
API calls, no cost, no keys needed).
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- Twilio (for sending/receiving WhatsApp messages) ---
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "")

    # --- Groq (conversation logic - LLM) ---
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # --- General settings ---
    APP_ENV: str = os.getenv("APP_ENV", "development")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8001")

    @property
    def is_mock_mode(self) -> bool:
        """
        If any required key is missing, run in mock mode
        (simulated responses instead of real API calls).
        """
        required_keys = [
            self.TWILIO_ACCOUNT_SID,
            self.GROQ_API_KEY,
        ]
        return not all(required_keys)


settings = Settings()
