from dotenv import load_dotenv
load_dotenv()
import os

# ==========================================
# TELEGRAM SETTINGS
# ==========================================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@TarunFitnessHub")

# Sirf aapka (owner ka) Telegram chat ID hi bot ko commands de sakega.
# Apna chat ID pata karne ka tarika README mein hai.
# Agar khaali chhoda to koi bhi jo bot ko message karega, wo agent use kar payega (NOT recommended).
OWNER_CHAT_ID = os.environ.get("OWNER_CHAT_ID", "")

# ==========================================
# AI + SEARCH API KEYS
# ==========================================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")      # console.groq.com se free key
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")        # serpapi.com se free key
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")  # unsplash.com/developers se free key

GROQ_MODEL = "llama-3.3-70b-versatile"

# ==========================================
# SUPABASE (Database)
# ==========================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# ==========================================
# AUTOMATIC CHANNEL POSTING SCHEDULE (agent ke alawa, ye background mein bhi chalta hai)
# ==========================================
POST_TIMES = ["09:00", "14:00", "20:00"]
TIMEZONE = "Asia/Kolkata"
CONTENT_ROTATION = ["trending_news", "quiz", "motivational"]

TRENDING_TOPICS = [
    "latest news India today",
    "trending technology news",
    "sports news today",
    "entertainment news today",
    "business news today",
]

# Keywords jinse agent samjhega ke aap chahte hain ye channel mein bhi post ho
CHANNEL_POST_KEYWORDS = [
    "channel", "post karo", "daal do", "daalo", "publish", "channel mein daal",
    "channel me daal", "post kar do", "upload karo",
]
