from dotenv import load_dotenv
import os

load_dotenv()

# ==========================
# Application
# ==========================
APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
ENVIRONMENT = os.getenv("ENVIRONMENT")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ==========================
# FastAPI
# ==========================
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT", 8000))

# ==========================
# JWT Authentication
# ==========================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)

# ==========================
# Redis
# ==========================
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# ==========================
# Logging
# ==========================
LOG_LEVEL = os.getenv("LOG_LEVEL")

# ==========================
# Fail-Fast Validation
# ==========================
required_settings = {
    "APP_NAME": APP_NAME,
    "HOST": HOST,
    "PORT": PORT,
    "SECRET_KEY": SECRET_KEY,
    "ALGORITHM": ALGORITHM,
}

for key, value in required_settings.items():
    if value in (None, ""):
        raise RuntimeError(f"{key} is not configured. Check your .env file.")