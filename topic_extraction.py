import openai
from collections import defaultdict
from config import CHAT_MODEL

def extract_topic(review_text):
    """Extract concise topic labels using LLM."""
    prompt = (
        f"Review: \"{review_text}\"\n"
        "Extract a concise topic label (a short phrase)."
    )
    response = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You summarize user feedback into topic labels."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=20,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()


def get_daily_topics(daily_reviews):
    daily_topics = defaultdict(list)
    for date_str, reviews in daily_reviews.items():
        for review_text in reviews:
            topic_label = extract_topic(review_text)
            daily_topics[date_str].append(topic_label)
    return daily_topics
