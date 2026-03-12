# ============================================================
#  TREND DETECTION — 3 Techniques on Time Series Data
# ============================================================

# ---------- Sample Data (Monthly Revenue in $K) ----------
revenue = [100, 130, 90, 120, 125, 130, 118, 135, 140, 128, 145, 150]
months  = ["Jan","Feb","Mar","Apr","May","Jun",
           "Jul","Aug","Sep","Oct","Nov","Dec"]


# ============================================================
# TECHNIQUE 1: MOVING AVERAGE
# — Smooths out noise so we can see the real direction
# ============================================================

def moving_average(data, window=3):
    ma = []
    for i in range(len(data)):
        if i < window - 1:
            ma.append(None)           # not enough data yet
        else:
            window_vals = data[i - window + 1 : i + 1]
            ma.append(sum(window_vals) / window)
    return ma


# ============================================================
# TECHNIQUE 2: SLOPE (Linear Regression)
# — Gives ONE number: direction + speed of the overall trend
# — Uses all data points, not just first and last
# ============================================================

def calculate_slope(data):
    n      = len(data)
    x_mean = (n - 1) / 2               # avg of indices 0,1,2...
    y_mean = sum(data) / n

    numerator   = sum((i - x_mean) * (data[i] - y_mean) for i in range(n))
    denominator = sum((i - x_mean) ** 2                  for i in range(n))

    slope = numerator / denominator
    return round(slope, 2)


# ============================================================
# TECHNIQUE 3: PERIOD COMPARISON
# — Splits data into two halves and compares % change
# — Tells you what's happening RIGHT NOW vs before
# ============================================================

def period_comparison(data, period=3):
    prev   = data[-(period * 2) : -period]   # e.g. months 7-9
    recent = data[-period:]                   # e.g. months 10-12

    prev_avg   = sum(prev)   / len(prev)
    recent_avg = sum(recent) / len(recent)

    pct_change = ((recent_avg - prev_avg) / prev_avg) * 100
    return round(prev_avg, 2), round(recent_avg, 2), round(pct_change, 2)


# ============================================================
#  RUN ALL 3 & PRINT RESULTS
# ============================================================

print("=" * 50)
print("       TREND DETECTION REPORT")
print("=" * 50)

# --- Raw Data ---
print("\n📊 Raw Revenue Data:")
for m, v in zip(months, revenue):
    print(f"   {m}: ${v}K")

# --- Moving Average ---
ma = moving_average(revenue, window=3)
print("\n📈 3-Month Moving Average:")
for m, v in zip(months, ma):
    val = f"${v:.1f}K" if v is not None else "  N/A (not enough data)"
    print(f"   {m}: {val}")

# --- Slope ---
# Run slope on smoothed data (ignore None values)
clean_ma = [v for v in ma if v is not None]
slope    = calculate_slope(clean_ma)
print(f"\n📐 Slope (on smoothed data): {slope}")
if slope > 0:
    print(f"   ✅ Trend is RISING  (+${slope}K per month on average)")
elif slope < 0:
    print(f"   ❌ Trend is FALLING  (-${abs(slope)}K per month on average)")
else:
    print(f"   ➡️  Trend is FLAT")

# --- Period Comparison ---
prev_avg, recent_avg, pct = period_comparison(revenue, period=3)
print(f"\n🔄 Period Comparison (last 3 vs previous 3 months):")
print(f"   Previous avg : ${prev_avg}K")
print(f"   Recent avg   : ${recent_avg}K")
print(f"   Change       : {'+' if pct > 0 else ''}{pct}%")
if pct > 0:
    print(f"   ✅ Revenue is ACCELERATING recently")
elif pct < 0:
    print(f"   ❌ Revenue is DECELERATING recently")
else:
    print(f"   ➡️  No change between periods")

print("\n" + "=" * 50)