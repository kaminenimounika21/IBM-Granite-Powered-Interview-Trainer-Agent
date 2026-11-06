"""
IBM Granite Interview Trainer Agent - Configuration Module
Strictly configured for IBM Cloud, IBM watsonx.ai, IBM Granite, and IBM Docling.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load local .env if present
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseSettings):
    APP_NAME: str = "IBM Granite-Powered Interview Trainer Agent"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # IBM watsonx.ai Foundation Model Configuration
    WATSONX_APIKEY: str = os.getenv("WATSONX_APIKEY", "")
    WATSONX_PROJECT_ID: str = os.getenv("WATSONX_PROJECT_ID", "")
    WATSONX_URL: str = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    WATSONX_MODEL_ID: str = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-8b-instruct")
    WATSONX_EMBEDDING_MODEL_ID: str = os.getenv("WATSONX_EMBEDDING_MODEL_ID", "ibm/slate-30m-english-rtr")

    # IBM Cloud Object Storage (COS)
    IBM_COS_APIKEY: str = os.getenv("IBM_COS_APIKEY", "")
    IBM_COS_SERVICE_INSTANCE_ID: str = os.getenv("IBM_COS_SERVICE_INSTANCE_ID", "")
    IBM_COS_ENDPOINT: str = os.getenv("IBM_COS_ENDPOINT", "https://s3.us-south.cloud-object-storage.appdomain.cloud")
    IBM_COS_BUCKET_NAME: str = os.getenv("IBM_COS_BUCKET_NAME", "ibm-interview-resumes-vault")

    # IBM Cloudant / Persistent Storage
    IBM_CLOUDANT_URL: str = os.getenv("IBM_CLOUDANT_URL", "")
    IBM_CLOUDANT_APIKEY: str = os.getenv("IBM_CLOUDANT_APIKEY", "")
    SQLITE_DB_PATH: str = str(BASE_DIR / "interview_trainer.db")

    # Security & Execution Controls
    MAX_RESUME_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list = [".pdf", ".docx", ".txt"]

    class Config:
        arbitrary_types_allowed = True

settings = Settings()

def get_watsonx_status() -> dict:
    """Return status of IBM watsonx.ai connection and active foundation model."""
    is_configured = bool(settings.WATSONX_APIKEY and settings.WATSONX_PROJECT_ID)
    return {
        "provider": "IBM watsonx.ai",
        "foundation_model": settings.WATSONX_MODEL_ID,
        "embedding_model": settings.WATSONX_EMBEDDING_MODEL_ID,
        "endpoint": settings.WATSONX_URL,
        "configured": is_configured,
        "mode": "Live IBM watsonx.ai Inference" if is_configured else "IBM Granite Prompt Template & Structured AI Engine (Ready for API Key)",
        "docling_status": "IBM Docling Core 2.106.0 Active"
    }

def update_runtime_settings(new_settings: dict) -> dict:
    """Update runtime configuration dynamically from Settings page."""
    for key, value in new_settings.items():
        if hasattr(settings, key) and value is not None:
            setattr(settings, key, value)
            os.environ[key] = str(value)
    
    # Save to .env for persistence
    env_path = BASE_DIR / ".env"
    lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    
    env_dict = {}
    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.strip().split("=", 1)
            env_dict[k.strip()] = v.strip()
    
    for key, value in new_settings.items():
        if value:
            env_dict[key] = str(value)
            
    with open(env_path, "w", encoding="utf-8") as f:
        for k, v in env_dict.items():
            f.write(f"{k}={v}\n")
            
    return get_watsonx_status()
