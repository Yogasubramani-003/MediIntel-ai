import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Use SQLite for local development without PostgreSQL
    database_url: str = Field(
        default=os.getenv(
            "DATABASE_URL",
            "sqlite:///./mediintel.db"  # SQLite instead of PostgreSQL
        )
    )

    upload_folder: str = Field(
        default=os.getenv(
            "UPLOAD_FOLDER",
            "./uploads"  # Local uploads folder
        )
    )

    debug: bool = Field(
        default=bool(os.getenv("DEBUG", True))  # Debug enabled for local dev
    )

    app_name: str = "MediIntel AI"


settings = Settings()
