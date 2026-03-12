import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

# ============================================================
# THIS IS YOUR GIVEN REVENUE DATA (from DB, CSV, etc.)
# In real world you would just load this:
#   df = pd.read_csv("revenue.csv")
# Here we are just hardcoding it to simulate that
# ============================================================

months = pd.date_range(start="2022-01", periods=36, freq="MS")

# This is the raw revenue as-is — no assumptions, no seasonal array
# You can see Mar, Nov, Dec are naturally high every year
revenue = [
    50200, 50800, 62500,  # Jan Feb Mar(surge)
    51000, 50500, 51200,  # Apr May Jun
    50800, 51500, 50900,  # Jul Aug Sep
    51100, 65300, 68100,  # Oct Nov(surge) Dec(surge)

    51500, 52000, 63200,  # Jan Feb Mar(surge)
    52500, 51800, 52100,  # Apr May Jun
    51900, 52800, 52200,  # Jul Aug Sep
    52400, 66100, 69500,  # Oct Nov(surge) Dec(surge)

    52800, 53200, 64100,  # Jan Feb Mar(surge)
    53500, 52900, 53400,  # Apr May Jun
    53100, 53800, 53500,  # Jul Aug Sep
    53700, 67200, 70800,  # Oct Nov(surge) Dec(surge)
]

df = pd.DataFrame({"total_revenue": revenue}, index=months)

print("Given Revenue Data:")
print(df.to_string())
print()

# ============================================================
# STL DECOMPOSITION
# Give it the revenue — it finds trend, seasonal, residual
# ============================================================

stl    = STL(df["total_revenue"], period=12)
result = stl.fit()

df["trend"]    = result.trend
df["seasonal"] = result.seasonal
df["residual"] = result.resid

# ============================================================
# PRINT RESULTS
# ============================================================

print(f"{'Month':<12} {'Total Revenue':>14}  {'Trend':>10}  {'Seasonal':>10}  {'Residual':>10}")
print("-" * 65)
for idx, row in df.iterrows():
    print(f"{str(idx.date()):<12} ${row['total_revenue']:>13,.0f}"
          f"  ${row['trend']:>9,.0f}"
          f"  ${row['seasonal']:>9,.0f}"
          f"  ${row['residual']:>9,.0f}")