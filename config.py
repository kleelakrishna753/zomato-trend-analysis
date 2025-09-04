from datetime import datetime

# App configuration
APP_ID = 'com.application.zomato'

# Date range for fetching reviews
START_DATE = datetime(2025, 5, 24)
END_DATE = datetime(2025, 5, 29)

# Trend analysis window
TREND_END = datetime(2025, 6, 2).date()
TREND_START = TREND_END - timedelta(days=15)

# Output file
OUTPUT_FILE = "zomato_review_trends.csv"

# OpenAI model configs
CHAT_MODEL = "gpt-3.5-turbo"
EMBED_MODEL = "text-embedding-3-small"
SIMILARITY_THRESHOLD = 0.8
