"""
Trend Detection Algorithm
=========================
Slope, Moving Average, Period Comparison, Quadrant Classification.
Logic ported from exploration/trend_detection_numpy_pandas.py

All calculations live here. No data defined here — data comes from backend/data/.
"""

import numpy as np
import pandas as pd
from typing import Optional

from data.dealerships import DEALERSHIPS, MONTHS


# ── Core calculation functions ────────────────────────────────────────────────

def compute_slope(x: np.ndarray, y: np.ndarray) -> float:
    slope, _ = np.polyfit(x, y, deg=1)
    return round(float(slope), 4)


def compute_trend_line(x: np.ndarray, y: np.ndarray) -> list[float]:
    slope, intercept = np.polyfit(x, y, deg=1)
    return [round(float(slope * xi + intercept), 2) for xi in x]


def compute_moving_average(values: list, window: int = 3) -> list[Optional[float]]:
    series = pd.Series(values).rolling(window=window).mean()
    return [None if np.isnan(v) else round(float(v), 2) for v in series]


def compute_period_change(values: list) -> dict:
    # Matches original script: months 7-9 (previous) vs 10-12 (recent)
    df = pd.DataFrame({"month": MONTHS, "revenue": values})
    prev = df[df["month"].between(7, 9)]["revenue"].mean()
    recent = df[df["month"].between(10, 12)]["revenue"].mean()
    change = recent - prev
    pct = (change / prev) * 100 if prev != 0 else 0
    return {
        "prev_avg": round(float(prev), 2),
        "recent_avg": round(float(recent), 2),
        "change": round(float(change), 2),
        "change_pct": round(float(pct), 2),
    }


def classify(slope: float, change_pct: float) -> dict:
    if slope > 0 and change_pct > 0:
        label = "CHAMPION"
        reason = "Upward long-term trend and positive recent momentum"
    elif slope < 0 and change_pct < 0:
        label = "STRAGGLER"
        reason = "Declining long-term trend and continued recent drop"
    elif slope > 0 and change_pct < 0:
        label = "AT RISK"
        reason = "Long-term growth but recent momentum has turned negative"
    else:
        label = "RECOVERING"
        reason = "Long-term decline but recent momentum is turning positive"
    return {"label": label, "reason": reason}


# ── Public API (called by routers) ───────────────────────────────────────────

def get_all_trends() -> dict:
    results = []
    x = np.array(MONTHS)

    for name, values in DEALERSHIPS.items():
        y = np.array(values)
        slope = compute_slope(x, y)
        period = compute_period_change(values)
        classification = classify(slope, period["change_pct"])

        results.append({
            "name": name,
            "months": MONTHS,
            "revenue": values,
            "trend_line": compute_trend_line(x, y),
            "moving_average": compute_moving_average(values, window=3),
            "slope": slope,
            "period_comparison": period,
            "classification": classification,
        })

    return {"dealerships": results}


def get_single_trend(name: str) -> dict:
    values = DEALERSHIPS[name]
    x = np.array(MONTHS)
    y = np.array(values)
    slope = compute_slope(x, y)
    period = compute_period_change(values)
    return {
        "name": name,
        "months": MONTHS,
        "revenue": values,
        "trend_line": compute_trend_line(x, y),
        "moving_average": compute_moving_average(values, window=3),
        "slope": slope,
        "period_comparison": period,
        "classification": classify(slope, period["change_pct"]),
    }
