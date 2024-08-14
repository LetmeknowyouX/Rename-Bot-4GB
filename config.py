import os

# Retrieve configuration from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
OWNER = os.environ.get("OWNER")
BOT_USERNAME = os.environ.get('BOT_USERNAME')

FORCE_SUBS = os.environ.get("FORCE_SUBS")
LOG_CHANNEL = os.environ.get("LOG_CHANNEL")

DB_URL = os.environ.get("DB_URL")
DB_NAME = os.environ.get("DB_NAME", "madflixbotz")

STRING = os.environ.get("STRING")
BOT_PIC = os.environ.get("BOT_PIC", "https://graph.org/file/ad48ac09b1e6f30d2dae4.jpg")

# Validate required variables
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")
if not API_ID:
    raise ValueError("API_ID environment variable is required")
if not API_HASH:
    raise ValueError("API_HASH environment variable is required")
if not OWNER:
    raise ValueError("OWNER environment variable is required")

# Convert to integer where applicable
try:
    API_ID = int(API_ID)
    OWNER = int(OWNER)
    LOG_CHANNEL = int(LOG_CHANNEL)
except ValueError:
    raise ValueError("API_ID, OWNER, and LOG_CHANNEL must be integers")

# Ensure database URL is provided if needed
if not DB_URL:
    raise ValueError("DB_URL environment variable is required")
