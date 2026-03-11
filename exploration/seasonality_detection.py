"""
Seasonality Detection — Learning Exercise
=======================================
Context:
Dealership sales naturally spike in Oct/Nov due to festivals.
If we don't understand seasonality, the system will raise false alarms
every November saying "Warning: Abnormal Spike!"

Concepts Covered:
  1. Seasonal Decomposition (breaking a line into Trend + Season + Residual)
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

# ─── 1. FAKE DATA WITH SEASONALITY ────────────────────────────
# Generate 3 years of monthly car sales (36 months)
np.random.seed(42)

dates = pd.date_range(start='2021-01-01', periods=36, freq='ME')
# Base trend is slowly growing from 100 to 150 cars sold per month
baseline_trend = np.linspace(100, 150, 36) 

# Seasonality: Oct (+30 cars), Nov (+40 cars), other months slightly negative
seasonality_pattern = np.array([-10, -15, 5, 10, -5, -10, 0, -5, 5, 30, 40, -10])
seasonality = np.tile(seasonality_pattern, 3) # Repeat for 3 years

# Random noise (e.g., a rainy day, sudden local construction)
noise = np.random.normal(0, 5, 36)

# Total Sales = Trend + Seasonality + Noise
sales = baseline_trend + seasonality + noise

df = pd.DataFrame({'sales': sales}, index=dates)

print("=" * 55)
print("1. CAR SALES DATA (Notice Oct/Nov spikes)")
print("=" * 55)
# Let's print the first year to see the spike
print(df.head(12).round(1).to_string())


# ─── 2. SEASONAL DECOMPOSITION ──────────────────────────────
# We use statsmodels to automatically break down our total sales
# model="additive" means: total = trend + seasonal + residual
# period=12 means: the cycle repeats exactly every 12 months

print("\n" + "=" * 55)
print("2. DECOMPOSING THE TIME SERIES")
print("=" * 55)

result = seasonal_decompose(df['sales'], model='additive', period=12)

# Pick a specific month that spiked to explain it. November 2022.
# Note: pd.date_range creates dates at the *end* of the month (e.g. 2022-11-30)
target_date = '2022-11-30'

obs  = result.observed.loc[target_date]
trnd = result.trend.loc[target_date]
seas = result.seasonal.loc[target_date]
res  = result.resid.loc[target_date]

print(f"Breakdown for {target_date} (Festival Month):")
print(f"  Observed Total Sales : {obs:.1f} cars")
print(f"  Underlying Trend     : {trnd:.1f} cars (Baseline if there were no festivals)")
print(f"  Seasonal expected    : +{seas:.1f} cars (The expected festival spike)")
print(f"  Unexpected (Residual): {res:+.1f} cars (The actual 'anomaly' or noise)")

print("""
-------------------------------------------------------
How this applies to JumpIQ:
-------------------------------------------------------
If sales jump massively in Nov, a naive "Outlier Agent" 
might flag November as a 'weird anomaly'.

But by calculating the `Seasonal component` (+40 cars), 
the Super Agent knows: 
"Ah, this +40 spike is completely normal for November!"

It will ONLY flag an anomaly if the `Residual` (unexpected) 
number is crazy high or crazy low. 
""")
