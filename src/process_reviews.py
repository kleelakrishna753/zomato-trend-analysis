import os
import openai
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_topics(reviews):
    """
    Use an LLM agent to extract consolidated topics from reviews.
    """
    if reviews.empty:
        return []

    combined_text = "\n".join(reviews['content'].tolist())

    prompt = f"""
    Analyze the following customer reviews and extract key issues, feature requests,
    or feedback topics. Consolidate similar feedback into a single category
    (e.g., 'Delivery partner rude', 'App crashing', 'Food quality bad').

    Reviews:
    {combined_text}

    Output a JSON list of topics with counts. Example:
    [
      {{"topic": "Delivery issue", "count": 12}},
      {{"topic": "Food stale", "count": 5}}
    ]
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response['choices'][0]['message']['content']
