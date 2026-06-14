import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Auto-detect: Use SQLite if PostgreSQL not available
    database_url: str = Field(
        default=os.getenv(
            "DATABASE_URL",
            "sqlite:///./mediintel.db"  # SQLite for local dev without PostgreSQL
        )
    )

    upload_folder: str = Field(
        default=os.getenv(
            "UPLOAD_FOLDER",
            "./uploads"  # Local uploads for dev
        )
    )

    debug: bool = Field(
        default=bool(os.getenv("DEBUG", True))
    )

    app_name: str = "MediIntel AI"


settings = Settings()