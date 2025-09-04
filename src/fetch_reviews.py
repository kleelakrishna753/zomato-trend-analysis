import pandas as pd
from google_play_scraper import Sort, reviews
import datetime

def fetch_reviews(app_id, target_date, lang="en", country="in", batch_size=100):
    """
    Fetch Google Play Store reviews for a given app_id and date.
    """
    result, _ = reviews(
        app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=batch_size
    )

    # Convert to DataFrame
    df = pd.DataFrame(result)
    df['date'] = pd.to_datetime(df['at']).dt.date

    # Filter reviews for the target_date
    target_date = datetime.datetime.strptime(target_date, "%Y-%m-%d").date()
    daily_reviews = df[df['date'] == target_date]

    return daily_reviews[['content', 'score', 'date']]