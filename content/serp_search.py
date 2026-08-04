import requests
from config import SERPAPI_KEY


def search_google(query, num_results=5):
    """
    SerpAPI ke through Google search results fetch karta hai.
    Returns: list of dicts with 'title', 'snippet', 'link'
    """
    try:
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google",
            "q": query,
            "gl": "in",
            "hl": "en",
            "num": num_results,
            "api_key": SERPAPI_KEY,
        }
        response = requests.get(url, params=params, timeout=20)
        data = response.json()

        results = []
        for item in data.get("organic_results", [])[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
            })
        return results
    except Exception as e:
        print(f"[serp_search] Error searching Google: {e}")
        return []


def search_news(query, num_results=10):
    """SerpAPI Google News engine - trending news ke liye."""
    try:
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_news",
            "q": query,
            "gl": "in",
            "hl": "en",
            "api_key": SERPAPI_KEY,
        }
        response = requests.get(url, params=params, timeout=20)
        data = response.json()

        stories = []
        for item in data.get("news_results", [])[:num_results]:
            source = item.get("source", {})
            stories.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "image": item.get("thumbnail"),
                "source": source.get("name", "News") if isinstance(source, dict) else "News",
            })
        return stories
    except Exception as e:
        print(f"[serp_search] Error searching news: {e}")
        return []
