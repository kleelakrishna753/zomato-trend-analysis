import sys
import json
from fetch_reviews import fetch_reviews
from process_reviews import extract_topics
from generate_report import update_trend_report

def main():
    app_id = "com.application.zomato"  # Zomato app ID
    target_date = "2025-06-01"  # Example date

    # 1. Fetch reviews
    reviews = fetch_reviews(app_id, target_date)

    if reviews.empty:
        print(f"No reviews found for {target_date}")
        return

    # 2. Extract topics
    topics_json = extract_topics(reviews)
    topics = json.loads(topics_json)

    # 3. Update trend report
    report = update_trend_report(topics, target_date)

    print("Trend report updated successfully!")
    print(report)

if __name__ == "__main__":
    main()
