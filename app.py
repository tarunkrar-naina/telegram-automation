import os
import json
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from config import POST_TIMES, TIMEZONE, CONTENT_ROTATION
from content.trending_news import get_trending_news_post
from content.quiz import get_quiz_post
from content.motivational import get_motivational_post
from telegram_poster import post_to_channel
from bot import process_telegram_update

app = Flask(__name__)

STATE_FILE = "rotation_state.json"

CONTENT_FUNCTIONS = {
    "trending_news": get_trending_news_post,
    "quiz": get_quiz_post,
    "motivational": get_motivational_post,
}


# ==========================================
# AUTO-POSTER (background scheduler, channel ke liye)
# ==========================================

def get_next_content_type():
    index = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                index = (state.get("last_index", -1) + 1) % len(CONTENT_ROTATION)
        except Exception:
            index = 0
    with open(STATE_FILE, "w") as f:
        json.dump({"last_index": index}, f)
    return CONTENT_ROTATION[index]


def run_scheduled_post():
    content_type = get_next_content_type()
    print(f"[scheduler] Running scheduled post. Content type: {content_type}")

    fetch_function = CONTENT_FUNCTIONS.get(content_type)
    content = fetch_function() if fetch_function else None

    if not content:
        print(f"[scheduler] {content_type} returned nothing, falling back to motivational.")
        content = get_motivational_post()

    success = post_to_channel(content)
    print(f"[scheduler] Post result: {'SUCCESS' if success else 'FAILED'}")


def setup_scheduler():
    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    for time_str in POST_TIMES:
        hour, minute = time_str.split(":")
        scheduler.add_job(
            run_scheduled_post,
            trigger=CronTrigger(hour=int(hour), minute=int(minute)),
            id=f"post_{time_str}",
        )
        print(f"[scheduler] Job scheduled for {time_str} {TIMEZONE}")
    scheduler.start()
    return scheduler


# ==========================================
# ROUTES
# ==========================================

@app.route("/")
def home():
    return {
        "status": "running",
        "message": "Telegram AI Agent is live!",
        "scheduled_channel_posts": POST_TIMES,
    }


@app.route("/webhook", methods=["POST"])
def webhook():
    """Telegram yahan har naya message bhejta hai."""
    update = request.get_json(force=True, silent=True)
    if update:
        process_telegram_update(update)
    return {"ok": True}


@app.route("/post-now")
def post_now():
    """Manual trigger - channel mein turant ek scheduled-style post karta hai."""
    run_scheduled_post()
    return {"status": "triggered", "message": "Check your Telegram channel."}


scheduler_instance = setup_scheduler()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
