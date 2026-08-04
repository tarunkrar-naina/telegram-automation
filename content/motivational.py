import requests
import random
from config import UNSPLASH_ACCESS_KEY

# Chhota sa built-in quotes pool (agar quote API fail ho to fallback)
QUOTES = [
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Your limitation—it's only your imagination.", "Unknown"),
    ("Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("Great things never come from comfort zones.", "Unknown"),
    ("Dream it. Wish it. Do it.", "Unknown"),
    ("Success doesn't just find you. You have to go out and get it.", "Unknown"),
    ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
    ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
]

SEARCH_TERMS = ["fitness motivation", "success", "nature sunrise", "workout gym", "mountains", "discipline"]


def get_motivational_post():
    """
    Unsplash se ek motivational/aesthetic image + quote caption banata hai.
    Returns: dict with 'caption' and 'image_url'
    """
    image_url = None
    try:
        query = random.choice(SEARCH_TERMS)
        url = "https://api.unsplash.com/photos/random"
        params = {
            "query": query,
            "orientation": "squarish",
            "client_id": UNSPLASH_ACCESS_KEY,
        }
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        image_url = data.get("urls", {}).get("regular")
    except Exception as e:
        print(f"[motivational.py] Error fetching image: {e}")

    quote, author = random.choice(QUOTES)
    caption = f"💪 *{quote}*\n\n— {author}\n\n#Motivation #DailyInspiration #StayStrong"

    return {
        "caption": caption,
        "image_url": image_url,
    }
