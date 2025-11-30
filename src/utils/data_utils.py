import pandas as pd
from datetime import timedelta
from typing import Dict, Any

def load_data(path: str, date_col: str, date_format: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df[date_col] = pd.to_datetime(df[date_col], format=date_format)
    return df

def compute_time_windows(df: pd.DataFrame, date_col: str, cfg: Dict[str, Any]) -> Dict[str, Any]:
    max_date = df[date_col].max()
    current_start = max_date - timedelta(days=cfg["time_window_days"] - 1)
    baseline_end = current_start - timedelta(days=1)
    baseline_start = baseline_end - timedelta(days=cfg["baseline_window_days"] - 1)
    return {
        "current": {"start": current_start, "end": max_date},
        "baseline": {"start": baseline_start, "end": baseline_end},
    }

def summarize_by_segment(df: pd.DataFrame, group_cols):
    grouped = df.groupby(group_cols).agg(
        impressions=("impressions", "sum"),
        spend=("spend", "sum"),
        clicks=("clicks", "sum"),
        purchases=("purchases", "sum"),
        revenue=("revenue", "sum"),
    ).reset_index()
    grouped["ctr"] = grouped["clicks"] / grouped["impressions"].replace(0, 1)
    grouped["roas"] = grouped["revenue"] / grouped["spend"].replace(0, 1)
    return grouped
