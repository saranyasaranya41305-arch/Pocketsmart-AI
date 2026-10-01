import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME = os.getenv("APP_NAME" "PocketSmart AI")
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key-in-production"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'data' / 'pocketsmart.db'}"
    )

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    USE_MOCK_AI = os.getenv(
        "USE_MOCK_AI",
        "true"
    ).lower() == "true"

    MAX_UPLOAD_MB = int(
        os.getenv("MAX_UPLOAD_MB", "5")
    )

    SESSION_COOKIE = "pocketsmart_token"


settings = Settings()