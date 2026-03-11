"""
Seasonality Detection — Beginner's Code Guide
=============================================
This script pairs with `seasonality_detection.md`.
It takes the exact same data from our Trend script (with 3 years of data so we can see repeating patterns)
and shows you exactly how to split "Normal Festival Spikes" from "Real Surprises".

Concepts:
  1. Creating Seasonal Data (Adding a fake October/November spike)
  2. Running `seasonal_decompose` (The magic statsmodels function)
  3. Proving that the "Surprise" (Residual) is what really matters.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# ─── 1. MAKE 3 YEARS OF FAKE DATA WITH FESTIVALS ──────────────────────────────
# We need more than 1 year for algorithms to "learn" what a repeating season looks like.
print("=" * 55)
print("1. GENERATING 3 YEARS OF DEALERSHIP SALES DATA")
print("=" * 55)

# 36 months of dates (Jan 2021 to Dec 2023)
dates = pd.date_range(start="2021-01-01", periods=36, freq="ME")

# A normal growing dealership trend (Starts at 210, grows to ~300)
base_trend = np.linspace(210, 300, 36)

# Create a repeating seasonal pattern:
# Most months are 0 (normal). October gets +40 cars, November gets +60 cars.
seasonality_pattern = [0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 60, 0] 
seasonality_3_years = np.tile(seasonality_pattern, 3) # Repeat it 3 times for 36 months

# Add some random life noise (maybe it rained one weekend, maybe a local ad worked well)
np.random.seed(42) # Keep the randomness the same every time we run this
noise = np.random.normal(0, 5, 36) 

# Combine them all together to simulate real life!
total_sales = base_trend + seasonality_3_years + noise

df = pd.DataFrame({
    "date": dates,
    "sales": total_sales
})
df.set_index("date", inplace=True) # Tell pandas that our 'date' column is the official timeline

# Let's peek at the first year. Notice how Oct and Nov jump massively compared to Sept.
print("\nYear 1 Sample:")
print(df.head(12).round(1))


# ─── 2. THE MAGIC ALGORITHM (seasonal_decompose) ──────────────────────────────
print("\n" + "=" * 55)
print("2. RUNNING SEASONAL DECOMPOSITION")
print("=" * 55)

# This one line does all the hard math.
# model='additive' means we assume:  Total = Trend + Season + Noise
# period=12 tells it that patterns repeat every 12 months.
decomposition = seasonal_decompose(df["sales"], model="additive", period=12)

# It gives us 3 new lists of numbers. Let's add them to our DataFrame so we can see them.
df["underlying_trend"] = decomposition.trend
df["expected_seasonality"] = decomposition.seasonal
df["unexpected_noise"] = decomposition.resid

# Let's look at November 2022 to prove it worked.
nov_2022 = df.loc["2022-11-30"]

print("\nLet's analyze what happened in November 2022:")
print(f"  Raw Total Cars Sold : {nov_2022['sales']:.1f}")
print(f"  Baseline Trend      : {nov_2022['underlying_trend']:.1f} (What they'd sell if no festivals existed)")
print(f"  Expected Festival   : {nov_2022['expected_seasonality']:.1f} (The algorithm learned Nov = +60 cars)")
print(f"  Unexpected Surprise : {nov_2022['unexpected_noise']:+.1f} (The true anomaly/residual noise)")

print("""
Why is the Surprise (Residual) only +1.9?
Because 251.2 (Trend) + 60.0 (Festival) = 311.2 expected cars.
They sold 313.1.
So the "surprise" is just an extra 1.9 cars. 
Even though 313 is massive, the system knows NOT to trigger an alarm.
""")


# ─── 3. LET'S FAKE AN ACTUAL DISASTER ─────────────────────────────────────────
print("=" * 55)
print("3. TESTING THE AGENT WITH A REAL PROBLEM")
print("=" * 55)

# Let's say in March 2023, the main road to the dealership was closed for construction.
# Sales plummet to 150 (way below normal).
df.loc["2023-03-31", "sales"] = 150

# Re-run the algorithm with the screwed up data
bad_decomposition = seasonal_decompose(df["sales"], model="additive", period=12)

# Check the new 'unexpected_noise' (Residual) for March 2023
march_2023_noise = bad_decomposition.resid.loc["2023-03-31"]

print(f"In March 2023, the dealership randomly sold only 150 cars.")
print(f"The algorithm calculates the 'Unexpected Surprise' (Residual) as: {march_2023_noise:.1f} cars!")
print("""
Because -122 is a massive negative number, the Outlier Agent will see this 
Residual and scream: "URGENT ANOMALY: Sales dropped 122 cars below expectations!"
""")

print("\nDone! Read through the code or the .md file to lock in the concepts.")
