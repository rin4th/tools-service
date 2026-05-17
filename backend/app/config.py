from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BASE_DIR.parent
STORAGE_DIR = PROJECT_DIR / "storage"
UPLOAD_DIR = STORAGE_DIR / "uploads"
OUTPUT_DIR = STORAGE_DIR / "outputs"
AVATAR_DIR = STORAGE_DIR / "avatars"

MAX_FILE_SIZE = 50 * 1024 * 1024
MAX_AVATAR_SIZE = 2 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_PDF_TYPES = {"application/pdf"}
ALLOWED_AVATAR_TYPES = {"image/jpeg", "image/png", "image/webp"}

for directory in (STORAGE_DIR, UPLOAD_DIR, OUTPUT_DIR, AVATAR_DIR):
    directory.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://pdftools:pdftools@localhost:5432/pdftools"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", case_sensitive=False)

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
