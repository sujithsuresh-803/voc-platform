import os
from dotenv import load_dotenv

# Load the .env file so Python can read your API key
load_dotenv()

# App settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

APP_TITLE = "Voice of Customer Intelligence Platform"
APP_ICON = "🎯"

# Analysis settings
MAX_FEEDBACK_ITEMS = 100  # Max items we analyse in one go