from datetime import datetime, timedelta

import pandas as pd

from src.core.database import engine


def read_metrics(groups_ids):
    df = pd.read_sql_query(
        'select * from "stats_postmetrics" where group_id = ANY(%(groups_ids)s) and timestamp >= %(timestamp)s',
        con=engine,
        params={
            "groups_ids": groups_ids,
            "timestamp": datetime.now() - timedelta(days=30)
        })

    df = df.drop(['id', 'post_id', 'timestamp'], axis=1)
    grouped = {
        group_id: group_df
        for group_id, group_df in df.groupby("group_id")
    }

    return grouped
