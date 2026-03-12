"""
Seasonality Detection Algorithm
================================
Seasonal decomposition using statsmodels (additive model).
Splits the signal into: observed / trend / seasonal / residual.

Logic mirrors exploration/script/seasonality_detection.py:
  - model='additive'  →  Total = Trend + Season + Noise
  - period=12          →  patterns repeat every 12 months
  - Residual analysis  →  flag real anomalies vs expected seasonal spikes

All calculations live here. No data defined here — data comes from backend/data/.
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from typing import Optional

from data.dealerships import DEALERSHIPS_3Y, MONTHS_3Y

# Annual seasonality — patterns repeat every 12 months.
# Requires 24+ data points (we have 36).
SEASONAL_PERIOD = 12


def _to_optional_list(arr) -> list[Optional[float]]:
    return [None if (v is None or np.isnan(v)) else round(float(v), 4) for v in arr]


def get_seasonality(dealership: str) -> dict:
    if dealership not in DEALERSHIPS_3Y:
        raise ValueError(
            f"Unknown dealership '{dealership}'. "
            f"Available: {list(DEALERSHIPS_3Y.keys())}"
        )

    values = DEALERSHIPS_3Y[dealership]
    dates = pd.date_range(start="2021-01-01", periods=len(values), freq="ME")
    series = pd.Series(values, index=dates)

    # The magic line — same as the script:
    # model='additive' means:  Total = Trend + Season + Noise
    # period=12 tells it that patterns repeat every 12 months.
    result = seasonal_decompose(series, model="additive", period=SEASONAL_PERIOD)

    seasonal_vals = np.array(result.seasonal.values, dtype=float)
    residual_vals = np.array(result.resid.values, dtype=float)
    observed_vals = np.array(result.observed.values, dtype=float)

    # --- Seasonal strength ---
    seasonal_strength = round(
        float(np.nanvar(seasonal_vals) / np.nanvar(observed_vals)) * 100, 1
    )

    # --- Peak / trough month (within a single 12-month cycle) ---
    # seasonal_decompose repeats the same 12-value pattern, so first 12 suffice.
    cycle = seasonal_vals[:12]
    peak_month = int(np.argmax(cycle)) + 1       # 1-indexed month
    trough_month = int(np.argmin(cycle)) + 1

    # --- Anomaly detection via residuals (from the script) ---
    # A large residual means something unexpected happened beyond trend + season.
    residual_std = float(np.nanstd(residual_vals))
    anomalies = []
    for i, r in enumerate(residual_vals):
        if not np.isnan(r) and abs(r) > 2 * residual_std:
            anomalies.append({
                "month_index": i + 1,
                "date": str(dates[i].date()),
                "residual": round(float(r), 2),
                "direction": "above" if r > 0 else "below",
            })

    return {
        "dealership": dealership,
        "months": MONTHS_3Y,
        "observed": values,
        "trend": _to_optional_list(result.trend.values),
        "seasonal": _to_optional_list(result.seasonal.values),
        "residual": _to_optional_list(result.resid.values),
        "anomalies": anomalies,
        "summary": {
            "model": "additive",
            "period": SEASONAL_PERIOD,
            "seasonal_strength_pct": seasonal_strength,
            "peak_month": peak_month,
            "trough_month": trough_month,
            "residual_std": round(residual_std, 2),
            "num_anomalies": len(anomalies),
        },
    }


def get_all_seasonality() -> dict:
    return {"dealerships": [get_seasonality(name) for name in DEALERSHIPS_3Y]}
