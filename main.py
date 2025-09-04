import openai
from fetch_reviews import fetch_reviews, group_reviews_by_date
from topic_extraction import get_daily_topics
from clustering import cluster_topics
from trend_analysis import consolidate_topics, generate_trend_table

def main():
    # Set OpenAI key
    openai.api_key = OPENAI_API_KEY  # <-- use env variable in production!

    # Step 1: Fetch reviews
    reviews = fetch_reviews()
    daily_reviews = group_reviews_by_date(reviews)

    # Step 2: Extract topics
    daily_topics = get_daily_topics(daily_reviews)

    # Step 3: Cluster topics
    unique_topics = set(topic for topics in daily_topics.values() for topic in topics)
    cluster_map = cluster_topics(unique_topics)

    # Step 4: Consolidate and analyze trends
    consolidated_daily = consolidate_topics(daily_topics, cluster_map)
    df_trends = generate_trend_table(consolidated_daily)

    print(df_trends.head())


if __name__ == "__main__":
    main()
