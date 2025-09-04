import pandas as pd
import os

def update_trend_report(new_topics, target_date, output_path="data/output/trend_report.csv"):
    """
    Update the trend report table (topics x last 30 days).
    """
    # Load or create report
    if os.path.exists(output_path):
        report = pd.read_csv(output_path, index_col=0)
    else:
        report = pd.DataFrame()

    # Ensure target_date column exists
    if target_date not in report.columns:
        report[target_date] = 0

    # Update counts
    for item in new_topics:
        topic = item["topic"]
        count = item["count"]

        if topic not in report.index:
            report.loc[topic] = 0

        report.loc[topic, target_date] = count

    # Keep last 30 days only
    if len(report.columns) > 30:
        report = report.iloc[:, -30:]

    # Save report
    report.to_csv(output_path)
    return report
