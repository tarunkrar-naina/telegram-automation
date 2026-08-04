import requests
import random
import html


def get_quiz_post():
    """
    Free trivia question fetch karta hai OpenTDB API se (no API key needed).
    Returns: dict with 'caption' and 'image_url' (None for quiz)
    """
    try:
        url = "https://opentdb.com/api.php?amount=1&type=multiple"
        response = requests.get(url, timeout=15)
        data = response.json()

        results = data.get("results", [])
        if not results:
            return None

        q = results[0]
        question = html.unescape(q["question"])
        correct = html.unescape(q["correct_answer"])
        incorrect = [html.unescape(a) for a in q["incorrect_answers"]]
        category = html.unescape(q.get("category", "General Knowledge"))

        options = incorrect + [correct]
        random.shuffle(options)

        labels = ["A", "B", "C", "D"]
        options_text = "\n".join(
            [f"{labels[i]}) {opt}" for i, opt in enumerate(options)]
        )

        correct_label = labels[options.index(correct)]

        caption = (
            f"🧠 *Quiz Time!* ({category})\n\n"
            f"{question}\n\n"
            f"{options_text}\n\n"
            f"⏳ Answer neeche comment mein batayein!\n"
            f"||Answer: {correct_label}) {correct}||\n\n"
            f"#Quiz #GK #TestYourKnowledge"
        )

        return {
            "caption": caption,
            "image_url": None,
        }
    except Exception as e:
        print(f"[quiz.py] Error fetching quiz: {e}")
        return None
