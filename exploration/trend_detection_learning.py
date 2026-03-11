"""
Trend Detection - Learning Exercise
====================================
Covers:
  1. Slope (linear regression on time index)
  2. Moving Average (smoothing + direction)
  3. Period Comparison (last 3 months vs previous 3 months)

No external libraries needed — pure Python.
Context: Fake dealership monthly revenue data ($k).
"""

# ─── FAKE DATA ─────────────────────────────────────────────────────────────────
# Monthly revenue ($k) for two dealerships over 12 months

months = list(range(1, 13))  # months 1 to 12

# "Champion" dealership — generally going up
champion_revenue: list[float] = [210, 215, 220, 218, 230, 235, 240, 238, 250, 255, 260, 265]

# "Straggler" dealership — generally going down
straggler_revenue: list[float] = [280, 275, 268, 260, 255, 250, 248, 240, 235, 228, 220, 215]


# ─── 1. SLOPE (Linear Regression) ──────────────────────────────────────────────
def compute_slope(values: list[float]):
    """
    Linear regression using the least-squares formula.
    x = time index (0, 1, 2, ...)
    y = revenue values

    slope m = ( n*sum(x*y) - sum(x)*sum(y) ) / ( n*sum(x^2) - sum(x)^2 )

    Returns: (slope, intercept)
    """
    n = len(values)
    x = list(range(n))                # time index: 0, 1, 2, ...

    sum_x   = sum(x)
    sum_y   = sum(values)
    sum_xy  = sum(xi * yi for xi, yi in zip(x, values))
    sum_x2  = sum(xi**2 for xi in x)

    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    b = (sum_y - m * sum_x) / n
    return m, b


print("=" * 55)
print("1. SLOPE (Linear Regression)")
print("=" * 55)

for name, data in [("Champion", champion_revenue), ("Straggler", straggler_revenue)]:
    slope, intercept = compute_slope(data)
    direction = "UP" if slope > 0 else "DOWN"
    print(f"\n{name}:")
    print(f"  Slope     = {slope:+.2f} $k / month  ->  {direction}")
    print(f"  Intercept = {intercept:.2f} $k")
    print(f"  Meaning   : Revenue changes by {slope:+.2f}$k each month on average.")

print("""
Key insight:
  slope > 0  =>  revenue growing   (Champion territory)
  slope < 0  =>  revenue declining  (Straggler territory)
  slope ~ 0  =>  flat / stable
""")


# ─── 2. MOVING AVERAGE ──────────────────────────────────────────────────────────
def moving_average(values: list[float], window: int = 3) -> list[float | None]:
    """
    For each position i >= window-1, average the last `window` values.
    Positions before that are None (not enough data yet).
    """
    result: list[float | None] = []
    result.extend([None] * (window - 1))
    for i in range(window - 1, len(values)):
        chunk = values[i - window + 1 : i + 1]  # type: ignore
        result.append(sum(chunk) / window)
    return result


print("=" * 55)
print("2. MOVING AVERAGE  (window = 3 months)")
print("=" * 55)

for name, data in [("Champion", champion_revenue), ("Straggler", straggler_revenue)]:
    ma = moving_average(data, window=3)
    print(f"\n{name}:")
    print(f"  {'Month':>5}  {'Raw $k':>7}  {'3-mo MA':>8}")
    print(f"  {'-----':>5}  {'------':>7}  {'-------':>8}")
    for i, (raw, avg) in enumerate(zip(data, ma)):
        avg_str = f"{avg:8.1f}" if avg is not None else "     n/a"
        print(f"  {i+1:>5}  {raw:>7}  {avg_str}")

print("""
Key insight:
  Raw data has noise (random ups/downs each month).
  Moving average smooths out that noise.
  If MA rises consistently  => uptrend signal.
  If MA falls consistently  => downtrend signal.
""")


# ─── 3. PERIOD COMPARISON ───────────────────────────────────────────────────────
def period_avg(values: list[float], start: int, end: int):
    """Average revenue over months [start..end] (1-indexed)."""
    return sum(values[start - 1 : end]) / (end - start + 1)  # type: ignore


print("=" * 55)
print("3. PERIOD COMPARISON  (last 3 vs previous 3 months)")
print("=" * 55)

for name, data in [("Champion", champion_revenue), ("Straggler", straggler_revenue)]:
    prev_avg = period_avg(data, start=7, end=9)    # months 7-9
    last_avg = period_avg(data, start=10, end=12)  # months 10-12
    change   = last_avg - prev_avg
    pct      = (change / prev_avg) * 100
    trend    = "GROWING" if change > 0 else "DECLINING"

    print(f"\n{name}:")
    print(f"  Months 7-9   avg = {prev_avg:.1f} $k   (previous period)")
    print(f"  Months 10-12 avg = {last_avg:.1f} $k   (recent period)")
    print(f"  Change           = {change:+.1f} $k  ({pct:+.1f}%)  ->  {trend}")

print("""
Key insight:
  Instead of looking at every data point, compare two windows.
  Positive change  =>  recent momentum is up.
  Negative change  =>  recent momentum is down.
  This is the simplest "trend" signal used in dashboards.
""")


# ─── PUTTING IT ALL TOGETHER ────────────────────────────────────────────────────
print("=" * 55)
print("COMBINED SIGNAL — Quadrant Classification")
print("=" * 55)

def classify(name: str, data: list[float]):
    slope, _   = compute_slope(data)
    prev_avg   = period_avg(data, 7, 9)
    last_avg   = period_avg(data, 10, 12)
    pct_change = (last_avg - prev_avg) / prev_avg * 100

    if slope > 0 and pct_change > 0:
        quadrant = "CHAMPION   (up trend + recent momentum)"
    elif slope < 0 and pct_change < 0:
        quadrant = "STRAGGLER  (down trend + recent decline)"
    elif slope > 0 and pct_change < 0:
        quadrant = "AT RISK    (long-term up, but recent dip)"
    else:
        quadrant = "RECOVERING (long-term down, but recent uptick)"

    print(f"\n{name}:")
    print(f"  Slope = {slope:+.2f},  Recent % change = {pct_change:+.1f}%")
    print(f"  => {quadrant}")

classify("Champion Dealership", champion_revenue)
classify("Straggler Dealership", straggler_revenue)

print("\nDone. Read the output top-to-bottom to follow the concepts.\n")
