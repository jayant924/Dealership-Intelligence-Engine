"""
Seasonality Detection Algorithm
================================
Seasonal decomposition using statsmodels (additive model).
Splits the signal into: observed / trend / seasonal / residual.

All calculations live here. No data defined here — data comes from backend/data/.
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from typing import Optional

from data.dealerships import DEALERSHIPS, MONTHS

# 12 data points → period=4 (quarterly) gives 3 full cycles.
# period=12 would need 24+ data points.
SEASONAL_PERIOD = 4


def _to_optional_list(arr) -> list[Optional[float]]:
    return [None if (v is None or np.isnan(v)) else round(float(v), 4) for v in arr]


def get_seasonality(dealership: str) -> dict:
    if dealership not in DEALERSHIPS:
        raise ValueError(
            f"Unknown dealership '{dealership}'. "
            f"Available: {list(DEALERSHIPS.keys())}"
        )

    values = DEALERSHIPS[dealership]
    series = pd.Series(values, index=pd.period_range("2024-01", periods=len(values), freq="M"))

    result = seasonal_decompose(series, model="additive", period=SEASONAL_PERIOD)

    seasonal_vals = np.array(result.seasonal.values, dtype=float)
    observed_vals = np.array(result.observed.values, dtype=float)

    seasonal_strength = round(
        float(np.nanvar(seasonal_vals) / np.nanvar(observed_vals)) * 100, 1
    )

    df_seasonal = pd.DataFrame({"month": MONTHS, "seasonal": seasonal_vals})
    peak_month = int(df_seasonal.loc[df_seasonal["seasonal"].idxmax(), "month"])
    trough_month = int(df_seasonal.loc[df_seasonal["seasonal"].idxmin(), "month"])

    return {
        "dealership": dealership,
        "months": MONTHS,
        "observed": values,
        "trend": _to_optional_list(result.trend.values),
        "seasonal": _to_optional_list(result.seasonal.values),
        "residual": _to_optional_list(result.resid.values),
        "summary": {
            "model": "additive",
            "period": SEASONAL_PERIOD,
            "seasonal_strength_pct": seasonal_strength,
            "peak_month": peak_month,
            "trough_month": trough_month,
        },
    }


def get_all_seasonality() -> dict:
    return {"dealerships": [get_seasonality(name) for name in DEALERSHIPS]}
