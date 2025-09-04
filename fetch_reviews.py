from google_play_scraper import reviews, Sort
from collections import defaultdict
from config import APP_ID, START_DATE, END_DATE

def fetch_reviews():
    """Fetch reviews between START_DATE and END_DATE."""
    all_reviews = []
    continuation_token = None
    stop_fetch = False

    while not stop_fetch:
        result, token = reviews(
            APP_ID,
            lang='en',
            country='in',
            sort=Sort.NEWEST,
            count=200,
            continuation_token=continuation_token
        )
        if not result:
            break

        for r in result:
            review_date = r['at']
            if review_date < START_DATE:
                stop_fetch = True
                break
            if START_DATE <= review_date <= END_DATE:
                all_reviews.append(r)

        continuation_token = token
        if continuation_token is None:
            break

    print(f"Fetched {len(all_reviews)} reviews.")
    return all_reviews


def group_reviews_by_date(all_reviews):
    daily_reviews = defaultdict(list)
    for r in all_reviews:
        date_str = r['at'].date().isoformat()
        daily_reviews[date_str].append(r['content'])
    return daily_reviews
