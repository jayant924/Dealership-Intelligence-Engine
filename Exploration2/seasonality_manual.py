import pandas as pd
import numpy as np


# ─── 1. REVENUE DATA WITH SEASONALITY ─────────────────────────
# Generate 3 years of monthly revenue (36 months)
np.random.seed(7)

monthly_index = pd.date_range(start='2022-01-01', periods=36, freq='ME')

# Base revenue grows steadily from 50000 to 80000 over 3 years
revenue_trend = np.linspace(50000, 80000, 36)

# Seasonality: Mar (+12000), Nov (+15000), Dec (+18000), rest are flat (0)
monthly_pattern = np.array([0, 0, 12000, 0, 0, 0, 0, 0, 0, 0, 15000, 18000])
revenue_seasonality = np.tile(monthly_pattern, 3)  # repeat for 3 years

# Random fluctuations (small day-to-day business variance)
fluctuation = np.random.normal(0, 800, 36)

# Total Revenue = Trend + Seasonality + Fluctuation
total_revenue = revenue_trend + revenue_seasonality + fluctuation

revenue_df = pd.DataFrame({'revenue': total_revenue}, index=monthly_index)

print("=" * 55)
print("1. MONTHLY REVENUE DATA (Notice Mar/Nov/Dec spikes)")
print("=" * 55)
print(revenue_df.head(36).round(1).to_string())