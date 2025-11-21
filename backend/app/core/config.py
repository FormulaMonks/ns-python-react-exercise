import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "FinTech Transaction Dashboard"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Placeholder for secret key - to be used in production
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")

settings = Settings()
