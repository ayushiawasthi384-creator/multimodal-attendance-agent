import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "multimodal-agent-secret-key-2026")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "0.0.0.0")

    # GenAI Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # Sustained Presence Tracking Thresholds
    # In seconds: time a student must continuously be detected to count as "PRESENT"
    SUSTAINED_PRESENCE_THRESHOLD_SEC = int(os.getenv("SUSTAINED_PRESENCE_THRESHOLD_SEC", 30))
    TRANSIENT_FILTER_WINDOW_SEC = int(os.getenv("TRANSIENT_FILTER_WINDOW_SEC", 15))
    SESSION_DURATION_DEFAULT_MIN = int(os.getenv("SESSION_DURATION_DEFAULT_MIN", 50))

    # Engagement Multimodal Weights
    WEIGHT_VISION = float(os.getenv("WEIGHT_VISION", 0.55))
    WEIGHT_AUDIO = float(os.getenv("WEIGHT_AUDIO", 0.35))
    WEIGHT_MOTION = float(os.getenv("WEIGHT_MOTION", 0.10))

    # Attention Drop Alert Threshold (Engagement score < 60 triggers intervention)
    ATTENTION_DROP_THRESHOLD = float(os.getenv("ATTENTION_DROP_THRESHOLD", 60.0))

    # Directories
    DATA_DIR = BASE_DIR / "data"
    STORAGE_DIR = BASE_DIR / "storage"
    AUDIO_STORAGE = STORAGE_DIR / "audio"
    CODE_STORAGE = STORAGE_DIR / "code"
    REPORTS_STORAGE = STORAGE_DIR / "reports"
    UPLOAD_FOLDER = BASE_DIR / "uploads"

    @classmethod
    def init_directories(cls):
        for path in [cls.DATA_DIR, cls.STORAGE_DIR, cls.AUDIO_STORAGE, cls.CODE_STORAGE, cls.REPORTS_STORAGE, cls.UPLOAD_FOLDER]:
            path.mkdir(parents=True, exist_ok=True)
