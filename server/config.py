from dotenv import load_dotenv
import os

load_dotenv()

# Настройки базы данных - для локальной разработки используем SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./giftpropaganda.db")

# Настройки Telegram Bot
TOKEN = os.getenv("TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN", "8429342375:AAFl55U3d2jiq3bm4UNTyDrbB0rztFTio2I")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://t-minigames.onrender.com")

# Настройки Redis (если используется)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Другие настройки
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Логирование для отладки
print(f"DATABASE_URL: {DATABASE_URL}")
print(f"TOKEN: {'SET' if TOKEN else 'NOT SET'}")
print(f"WEBHOOK_URL: {WEBHOOK_URL}")
