from agent import handle_user_message
from telegram_poster import send_message
from config import OWNER_CHAT_ID


def process_telegram_update(update):
    """
    Telegram se aane wale har update ko process karta hai.
    Sirf text messages handle karta hai (private chat se).
    """
    message = update.get("message")
    if not message:
        return

    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id or not text:
        return

    # Security: agar OWNER_CHAT_ID set hai, to sirf wahi user agent use kar sakta hai
    if OWNER_CHAT_ID and str(chat_id) != str(OWNER_CHAT_ID):
        send_message(chat_id, "Sorry, ye agent sirf apne owner ke liye kaam karta hai.")
        return

    # Simple /start command
    if text.strip() == "/start":
        send_message(
            chat_id,
            "Namaste! Main aapka personal Telegram AI Agent hoon 🤖\n\n"
            "Mujhe kuch bhi bolein — jaise:\n"
            "- 'Aaj ki top tech news batao'\n"
            "- 'Ye news channel mein post karo'\n"
            "- 'Best protein powder kaunsa hai India mein'\n\n"
            "Main Google search karke aur AI se sochkar jawab dunga!"
        )
        return

    try:
        reply, posted_to_channel = handle_user_message(chat_id, text)
        if posted_to_channel:
            reply += "\n\n✅ Ye channel mein bhi post ho gaya hai."
        send_message(chat_id, reply)
    except Exception as e:
        print(f"[bot] Error processing message: {e}")
        send_message(chat_id, "Kuch error aa gaya, thodi der baad try karein.")
