from groq_client import call_groq


def write_news_caption(title, snippet, source):
    """Raw news ko ek ready-to-post Telegram caption mein badalta hai."""
    prompt = (
        f"Neeche di gayi news ko ek short, engaging Telegram channel post mein badlo.\n\n"
        f"Title: {title}\n"
        f"Details: {snippet}\n"
        f"Source: {source}\n\n"
        f"Rules:\n"
        f"- Hinglish mein likho\n"
        f"- Ek achha hook line se shuru karo\n"
        f"- 2-4 lines ka summary\n"
        f"- 3-5 emojis use karo\n"
        f"- End mein 3-4 relevant hashtags\n"
        f"- Sirf caption text do, koi extra explanation nahi"
    )

    messages = [{"role": "user", "content": prompt}]
    caption = call_groq(messages, temperature=0.8, max_tokens=400)

    if not caption:
        caption = f"📰 {title}\n\n{snippet}\n\nSource: {source}\n\n#News #Updates #Trending"

    return caption
