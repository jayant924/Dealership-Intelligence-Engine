"""
Trend Detection — with NumPy & Pandas
=======================================
Same 3 concepts as before, now using the real tools.
Beginner-friendly: every line is explained.

Concepts:
  1. Slope  (numpy)
  2. Moving Average  (pandas)
  3. Period Comparison  (pandas)
"""

import numpy as np
import pandas as pd


# ─── FAKE DATA ────────────────────────────────────────────────────────────────
# Think of a DataFrame as an Excel table.
# Each row = one month. Each column = one dealership's revenue.

df = pd.DataFrame({
    "month":     list(range(1, 13)),
    "champion":  [210, 215, 220, 218, 230, 235, 240, 238, 250, 255, 260, 265],
    "straggler": [280, 275, 268, 260, 255, 250, 248, 240, 235, 228, 220, 215],
})

print("=" * 55)
print("OUR DATA  (monthly revenue in $k)")
print("=" * 55)
print(df.to_string(index=False))
# index=False  =>  hides the row numbers on the left (cleaner output)


# ─── 1. SLOPE ─────────────────────────────────────────────────────────────────
# np.polyfit(x, y, deg=1) fits a straight line through the data.
# deg=1  means degree-1 polynomial = straight line  (y = mx + b)
# It returns [slope, intercept].

print("\n" + "=" * 55)
print("1. SLOPE  (np.polyfit)")
print("=" * 55)

x = df["month"].values          # array([1, 2, 3, ..., 12])
# .values converts the pandas column into a plain numpy array — polyfit needs that

for name in ["champion", "straggler"]:
    y = df[name].values          # revenue numbers as a numpy array

    slope, intercept = np.polyfit(x, y, deg=1)
    # polyfit does the heavy maths (same formula we wrote by hand before)
    # and returns the two numbers that define the best-fit line

    direction = "UP" if slope > 0 else "DOWN"
    print(f"\n{name.upper()}:")
    print(f"  slope     = {slope:+.2f} $k per month  ->  {direction}")
    print(f"  intercept = {intercept:.2f} $k")
    print(f"  meaning   : On average, revenue changes by {slope:+.2f}$k each month.")

print("""
Rule of thumb:
  slope > 0  ->  growing    (Champion)
  slope < 0  ->  declining  (Straggler)
  slope ~ 0  ->  flat
""")


# ─── 2. MOVING AVERAGE ────────────────────────────────────────────────────────
# pandas .rolling(window=3).mean()
#   - rolling(3)   : slide a 3-row window across the column
#   - .mean()      : average the 3 values inside that window
# First 2 rows become NaN (not enough history yet) — same as None before.

print("=" * 55)
print("2. MOVING AVERAGE  (pandas rolling)")
print("=" * 55)

# Add new MA columns directly to the DataFrame
df["champion_ma3"]  = df["champion"].rolling(window=3).mean()
df["straggler_ma3"] = df["straggler"].rolling(window=3).mean()

# round(1)  ->  show 1 decimal place
print("\nChampion — raw vs 3-month moving average:")
print(df[["month", "champion", "champion_ma3"]].round(1).to_string(index=False))

print("\nStraggler — raw vs 3-month moving average:")
print(df[["month", "straggler", "straggler_ma3"]].round(1).to_string(index=False))

print("""
Notice:
  Raw values jump around (noise).
  The MA column rises/falls more smoothly (signal).
  NaN in rows 1-2 = not enough data yet for a 3-month window.
""")


# ─── 3. PERIOD COMPARISON ─────────────────────────────────────────────────────
# We split the year into two halves and compare average revenue.
# pandas boolean indexing:  df[df["month"] >= 10]
#   ->  keeps only rows where month is 10, 11, or 12

print("=" * 55)
print("3. PERIOD COMPARISON  (last 3 vs previous 3 months)")
print("=" * 55)

# Filter rows into two groups
prev_period = df[df["month"].between(7, 9)]   # months 7, 8, 9
last_period = df[df["month"].between(10, 12)] # months 10, 11, 12
# .between(a, b) is the same as (df["month"] >= a) & (df["month"] <= b)

for name in ["champion", "straggler"]:
    prev_avg = prev_period[name].mean()   # average of 3 values
    last_avg = last_period[name].mean()

    change = last_avg - prev_avg
    pct    = (change / prev_avg) * 100
    trend  = "GROWING" if change > 0 else "DECLINING"

    print(f"\n{name.upper()}:")
    print(f"  months 7-9   avg = {prev_avg:.1f} $k   (previous period)")
    print(f"  months 10-12 avg = {last_avg:.1f} $k   (recent period)")
    print(f"  change           = {change:+.1f} $k  ({pct:+.1f}%)  ->  {trend}")

print("""
Positive %  ->  recent momentum is up.
Negative %  ->  recent momentum is down.
""")


# ─── COMBINED SIGNAL ──────────────────────────────────────────────────────────
print("=" * 55)
print("COMBINED -> Quadrant Classification")
print("=" * 55)

def classify(name):
    y     = df[name].values
    x     = df["month"].values
    slope, _ = np.polyfit(x, y, deg=1)

    prev_avg = df[df["month"].between(7, 9)][name].mean()
    last_avg = df[df["month"].between(10, 12)][name].mean()
    pct      = (last_avg - prev_avg) / prev_avg * 100

    if slope > 0 and pct > 0:
        label = "CHAMPION    (up trend + recent momentum)"
    elif slope < 0 and pct < 0:
        label = "STRAGGLER   (down trend + recent decline)"
    elif slope > 0 and pct < 0:
        label = "AT RISK     (long-term up, but recent dip)"
    else:
        label = "RECOVERING  (long-term down, but recent uptick)"

    print(f"\n{name.upper()}:")
    print(f"  slope = {slope:+.2f},  recent change = {pct:+.1f}%")
    print(f"  -> {label}")

classify("champion")
classify("straggler")

print("\nDone!\n")
