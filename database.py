import hashlib
from datetime import datetime, timezone
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

_client: Client = None


def get_client():
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("[database] Supabase credentials missing.")
            return None
        try:
            _client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            print(f"[database] Failed to connect: {e}")
            return None
    return _client


def make_hash(text):
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()


# ---------- Posted content (duplicate-check for auto channel posts) ----------

def is_duplicate(title):
    client = get_client()
    if client is None:
        return False
    content_hash = make_hash(title)
    try:
        result = client.table("posted_content").select("id").eq("content_hash", content_hash).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"[database] Error checking duplicate: {e}")
        return False


def log_post(title, content_type):
    client = get_client()
    if client is None:
        return
    content_hash = make_hash(title)
    try:
        client.table("posted_content").insert({
            "content_hash": content_hash,
            "title": title[:500],
            "content_type": content_type,
            "posted_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception as e:
        print(f"[database] Error logging post: {e}")


# ---------- Chat history (agent conversation memory) ----------

def save_chat_message(chat_id, role, content):
    """role: 'user' ya 'assistant'"""
    client = get_client()
    if client is None:
        return
    try:
        client.table("chat_history").insert({
            "chat_id": str(chat_id),
            "role": role,
            "content": content[:2000],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception as e:
        print(f"[database] Error saving chat message: {e}")


def get_recent_history(chat_id, limit=6):
    """Pichli 'limit' messages laata hai taaki agent ko conversation ka context mile."""
    client = get_client()
    if client is None:
        return []
    try:
        result = (
            client.table("chat_history")
            .select("role, content")
            .eq("chat_id", str(chat_id))
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        rows = result.data or []
        rows.reverse()  # chronological order mein wapas
        return rows
    except Exception as e:
        print(f"[database] Error fetching history: {e}")
        return []
