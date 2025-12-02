import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Skill-Match"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL: str = os.getenv("MISTRAL_MODEL", "open-mixtral-8x7b")
    
    # CORS Origins
    _origins_str = os.getenv("ALLOWED_ORIGINS", "")
    # Nettoyage de la chaîne (suppression des crochets et guillemets si format JSON/liste)
    _origins_str = _origins_str.replace("[", "").replace("]", "").replace('"', "").replace("'", "")
    
    ALLOWED_ORIGINS: list = [
        origin.strip() for origin in _origins_str.split(",") if origin.strip()
    ] or [
        "http://localhost:8080",
        "https://skill-match-iota.vercel.app",
        "https://skill-match-iota.vercel.app/"
    ]
    
    # Parsing
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: set = {"pdf", "docx", "txt"}

settings = Settings()

