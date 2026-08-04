import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_message(chat_id, text):
    """Kisi bhi chat (user ya group) ko simple text reply bhejta hai."""
    try:
        response = requests.post(
            f"{BASE_URL}/sendMessage",
            data={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=20,
        )
        result = response.json()
        if not result.get("ok"):
            # Markdown parsing fail ho sakti hai kabhi kabhi, plain text try karo
            response = requests.post(
                f"{BASE_URL}/sendMessage",
                data={"chat_id": chat_id, "text": text},
                timeout=20,
            )
            result = response.json()
        return result.get("ok", False)
    except Exception as e:
        print(f"[telegram_poster] Error sending message: {e}")
        return False


def post_to_channel(content):
    """
    content: dict with 'caption' and optional 'image_url'
    Aapke fixed Telegram channel mein post karta hai.
    """
    if not content:
        print("[telegram_poster] Empty content, skipping channel post.")
        return False

    caption = content.get("caption", "")
    image_url = content.get("image_url")

    try:
        if image_url:
            endpoint = f"{BASE_URL}/sendPhoto"
            payload = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "photo": image_url,
                "caption": caption,
                "parse_mode": "Markdown",
            }
        else:
            endpoint = f"{BASE_URL}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": caption,
                "parse_mode": "Markdown",
            }

        response = requests.post(endpoint, data=payload, timeout=20)
        result = response.json()

        if result.get("ok"):
            print("[telegram_poster] Channel post successful!")
            return True

        print(f"[telegram_poster] Telegram API error: {result}")
        if image_url:
            fallback_payload = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": caption,
                "parse_mode": "Markdown",
            }
            fallback_resp = requests.post(f"{BASE_URL}/sendMessage", data=fallback_payload, timeout=20)
            return fallback_resp.json().get("ok", False)
        return False

    except Exception as e:
        print(f"[telegram_poster] Exception while posting to channel: {e}")
        return False


# Backward-compatible alias (auto-poster scheduler isko use karta hai)
post_to_telegram = post_to_channel
