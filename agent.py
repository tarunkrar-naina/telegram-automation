from groq_client import call_groq
from content.serp_search import search_google
from database import save_chat_message, get_recent_history
from telegram_poster import post_to_channel
from config import CHANNEL_POST_KEYWORDS

SYSTEM_PROMPT = (
    "Tum Tarun ke personal Telegram assistant ho, jiska naam 'Fitness Hub Agent' hai. "
    "Tum Hinglish mein baat karte ho (Hindi + English mix, jaisa log casually likhte hain). "
    "Tumhe web search results diye jaate hain jab relevant ho — unko use karke accurate, "
    "up-to-date jawab do. Agar user kisi cheez ko channel mein post karne ko bole, "
    "to ek achha Telegram-ready caption bhi banao (emojis aur hashtags ke saath). "
    "Jawab short aur useful rakho, zyada lamba mat likho jab tak zaroori na ho."
)


def wants_channel_post(text):
    lowered = text.lower()
    return any(keyword in lowered for keyword in CHANNEL_POST_KEYWORDS)


def should_search(text):
    """Chhoti greetings ke liye search skip karo, baaki sab ke liye search karo."""
    lowered = text.strip().lower()
    skip_words = ["hi", "hello", "hey", "kaise ho", "thanks", "thank you", "ok", "okay"]
    return len(lowered) > 8 and not any(lowered == w for w in skip_words)


def build_context_messages(chat_id, user_text, search_results):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Pichli conversation ka context add karo
    history = get_recent_history(chat_id, limit=6)
    for row in history:
        messages.append({"role": row["role"], "content": row["content"]})

    # Agar search results hain, unhe context ke roop mein add karo
    if search_results:
        search_context = "\n\n".join(
            [f"- {r['title']}: {r['snippet']}" for r in search_results]
        )
        user_content = (
            f"Web search results:\n{search_context}\n\n"
            f"User ka message: {user_text}"
        )
    else:
        user_content = user_text

    messages.append({"role": "user", "content": user_content})
    return messages


def handle_user_message(chat_id, user_text):
    """
    Main agent function:
    1. Zaroorat pade to Google search karta hai (SerpAPI)
    2. Groq ko context ke saath call karta hai
    3. Reply generate karta hai
    4. Agar user ne channel-post ka ishara diya, to channel mein bhi post karta hai
    5. Conversation history Supabase mein save karta hai
    """
    save_chat_message(chat_id, "user", user_text)

    search_results = search_google(user_text, num_results=5) if should_search(user_text) else []

    messages = build_context_messages(chat_id, user_text, search_results)
    reply = call_groq(messages)

    if not reply:
        reply = "Sorry, abhi thodi dikkat aa rahi hai processing mein. Thodi der baad try karein."

    save_chat_message(chat_id, "assistant", reply)

    # Agar user ne channel mein post karne ko kaha, to reply ko channel mein bhi bhejo
    posted_to_channel = False
    if wants_channel_post(user_text):
        posted_to_channel = post_to_channel({"caption": reply, "image_url": None})

    return reply, posted_to_channel
