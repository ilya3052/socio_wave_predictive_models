from datetime import datetime, timedelta

import pandas as pd
from icecream import ic

from src.core.database import engine


def read_metrics(groups_ids):
    df = pd.read_sql_query(
        """
        select * from (
            select *, row_number() over (
                partition by group_id order by post_id desc
            ) as rn
            from "stats_postmetrics"
            where group_id = ANY(%(groups_ids)s)
              and timestamp >= %(timestamp)s
        ) sub where rn <= %(limit)s
        order by post_id desc
        """,
        con=engine,
        params={
            "groups_ids": groups_ids,
            "timestamp": datetime.now() - timedelta(days=30),
            "limit": 500
        })
    df = df.drop(['id', 'post_id', 'timestamp', 'rn'], axis=1)
    grouped = {
        group_id: group_df
        for group_id, group_df in df.groupby("group_id")
    }

    return grouped
