import pandas as pd
from collections import defaultdict
from config import TREND_START, TREND_END, OUTPUT_FILE

def consolidate_topics(daily_topics, cluster_map):
    consolidated_daily = defaultdict(list)
    for date_str, topics in daily_topics.items():
        for topic in topics:
            rep = cluster_map.get(topic, topic)
            consolidated_daily[date_str].append(rep)
    return consolidated_daily


def generate_trend_table(consolidated_daily):
    date_range = [(TREND_START + pd.Timedelta(days=i)).isoformat() for i in range((TREND_END - TREND_START).days + 1)]
    topic_counts = defaultdict(lambda: {date: 0 for date in date_range})

    for date_str, topics in consolidated_daily.items():
        if date_str in date_range:
            for topic in topics:
                topic_counts[topic][date_str] += 1

    df_trends = pd.DataFrame.from_dict(topic_counts, orient='index')
    df_trends = df_trends[date_range]  # keep column order
    df_trends.to_csv(OUTPUT_FILE)
    print(f"Trend table saved to {OUTPUT_FILE}")
    return df_trends
