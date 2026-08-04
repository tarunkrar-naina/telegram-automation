import requests
from config import GROQ_API_KEY, GROQ_MODEL

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_groq(messages, temperature=0.7, max_tokens=700):
    """
    Groq API ko messages (OpenAI-style chat format) bhejta hai aur reply text return karta hai.
    messages example: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    """
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        data = response.json()

        if "choices" not in data:
            print(f"[groq_client] Unexpected response: {data}")
            return None

        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[groq_client] Error calling Groq: {e}")
        return None
