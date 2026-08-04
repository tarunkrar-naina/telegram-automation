import random
from content.serp_search import search_news
from content.news_writer import write_news_caption
from database import is_duplicate, log_post
from config import TRENDING_TOPICS


def get_trending_news_post():
    query = random.choice(TRENDING_TOPICS)
    stories = search_news(query, num_results=10)

    if not stories:
        print("[trending_news] No stories fetched from SerpAPI.")
        return None

    for story in stories:
        title = story.get("title", "")
        if not title:
            continue

        if is_duplicate(title):
            print(f"[trending_news] Skipping duplicate: {title[:60]}")
            continue

        caption = write_news_caption(
            title=title,
            snippet=story.get("snippet", ""),
            source=story.get("source", "News"),
        )

        log_post(title, "trending_news")

        return {
            "caption": caption,
            "image_url": story.get("image"),
        }

    print("[trending_news] All fetched stories were duplicates.")
    return None
