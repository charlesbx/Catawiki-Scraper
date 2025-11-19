"""
Configuration module for Catawiki Scraper.
Uses environment variables for sensitive data.
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_IDS: List[str] = os.getenv("TELEGRAM_CHAT_IDS", "").split(",")

# Validate required configuration
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
if not TELEGRAM_CHAT_IDS or TELEGRAM_CHAT_IDS == [""]:
    raise ValueError("TELEGRAM_CHAT_IDS environment variable is required")

# Scraper Configuration
CATAWIKI_BASE_URL: str = os.getenv(
    "CATAWIKI_BASE_URL",
    "https://www.catawiki.com/fr/c/333-montres"
)
SCRAPER_MAX_ITEMS: int = int(os.getenv("SCRAPER_MAX_ITEMS", "300"))
SCRAPER_SCROLL_DELAY: float = float(os.getenv("SCRAPER_SCROLL_DELAY", "0.05"))
SCRAPER_PAGE_LOAD_DELAY: float = float(os.getenv("SCRAPER_PAGE_LOAD_DELAY", "0.25"))

# Browser Configuration
CHROME_BINARY: str = os.getenv("CHROME_BINARY", "/usr/bin/chromium")
CHROMEDRIVER_BINARY: str = os.getenv("CHROMEDRIVER_BINARY", "/usr/bin/chromedriver")
HEADLESS_MODE: bool = os.getenv("HEADLESS_MODE", "true").lower() == "true"

# Filtering Thresholds
PERCENTAGE_THRESHOLD: float = float(os.getenv("PRICE_PERCENTAGE_THRESHOLD", "0.90"))
REMAINING_TIME_THRESHOLD: int = int(os.getenv("REMAINING_TIME_THRESHOLD", "1800"))

# Storage
DATA_FILE: str = os.getenv("DATA_FILE", "items.json")

# Logging
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE: str = os.getenv("LOG_FILE", "catawiki_scraper.log")

# Backward compatibility (deprecated - will be removed)
TelegramChatID = TELEGRAM_CHAT_IDS
TelegramToken = TELEGRAM_BOT_TOKEN