# Trend Detection (Manager Brief) — JumpIQ

Purpose: Meeting-friendly explanation of the **Trend Detection** algorithm used in this project, in simple language (with just enough math to be credible).

**Source of truth (code):**
- Backend implementation: `exploration/web app/backend/algorithms/trend.py`
- Explained script: `exploration/script/trend_detection.py`
- Detailed technical doc: `docs/algorithms/trend_detection.md`

---

## 1) Problem statement (simple)

We have monthly revenue for each dealership (e.g., month 1 to 12).

We want to answer two very practical questions:

- **Long-term direction:** “Overall year me revenue up ja raha hai ya down?”
- **Recent momentum:** “Last 3 months me situation improve hui ya worse?”

Because raw monthly data is noisy (upar-neeche hota rehta hai), we use a small set of **interpretable signals**.

---

## 2) What data goes in?

For each dealership:

- **months**: `[1..12]` (currently 12 months in backend dataset)
- **revenue**: e.g., `[210, 215, 220, ...]` in $k

---

## 3) What results come out?

For each dealership we compute:

- **slope**: average change per month (e.g., `+5.0 $k/mo` or `-3.2 $k/mo`)
- **trend_line**: the straight line values used to visualize the slope
- **moving_average (MA3)**: 3-month moving average (smooth version of revenue)
- **period_comparison**: previous avg (months 7–9) vs recent avg (months 10–12)
- **classification**: one of `CHAMPION / STRAGGLER / AT RISK / RECOVERING` + a human-readable reason

These are exactly the fields returned by the API (`/api/trends`).

---

## 4) The 3 signals (foundation concepts)

### A) Slope (overall direction)
Think of revenue plotted on a chart. We draw the **best-fit straight line** through the points.

That line is:  \[
revenue \approx slope \times month + intercept
\]

- **slope > 0** ⇒ overall upward direction (good)
- **slope < 0** ⇒ overall downward direction (concerning)

In code we use `numpy.polyfit(..., deg=1)` which is standard linear regression fitting.

---

### B) Moving average (noise smoothing)
Monthly values can jump. MA3 reduces noise:

- MA3 at month 3 = average of months (1,2,3)
- MA3 at month 4 = average of months (2,3,4)
- …and so on

This helps the chart show signal more clearly, but **MA lags** a bit (that’s expected).

In code we use `pandas.Series(...).rolling(window=3).mean()`.

---

### C) Period comparison (recent momentum)
Managers care a lot about “recent” performance.

So we compare:

- **Previous period:** months 7–9 average
- **Recent period:** months 10–12 average

Then compute:

- **change = recent_avg - prev_avg**
- **change_pct = change / prev_avg × 100**

If `change_pct` is positive, recent momentum is improving.

---

## 5) The classification logic (the quadrant)

We combine **(Slope)** and **(Recent momentum %)** to assign a label:

- **CHAMPION**: slope \(> 0\) AND change_pct \(> 0\)  
  “Long-term up + recent up”

- **STRAGGLER**: slope \(< 0\) AND change_pct \(< 0\)  
  “Long-term down + recent down”

- **AT RISK**: slope \(> 0\) AND change_pct \(< 0\)  
  “Long-term up, but recent dip (watchlist)”

- **RECOVERING**: slope \(< 0\) AND change_pct \(> 0\)  
  “Long-term down, but recent improvement”

This is deliberately simple and explainable — so we can defend it in business reviews.

---

## 6) Example (intuitive)

Imagine two dealerships:

### Dealership A (Champion-like)
- Over 12 months revenue slowly rises
- Last 3 months average is higher than months 7–9 average

Result:
- slope: positive
- change_pct: positive
- classification: **CHAMPION**

### Dealership B (Straggler-like)
- Over 12 months revenue slowly falls
- Last 3 months average is lower than months 7–9 average

Result:
- slope: negative
- change_pct: negative
- classification: **STRAGGLER**

Even without “black-box AI”, stakeholders can immediately understand *why* the label was assigned.

---

## 7) Why this is a good “Phase-1” approach

- **Interpretable:** Every number has a story (direction, momentum, smoothing).
- **Fast + stable:** Simple math, low compute, low risk of overfitting.
- **Debrief-friendly:** Easy to explain in meetings and dashboards.
- **Extensible:** Later we can add seasonality/outlier agents without breaking the logic.

This matches the design principle in `docs/AGENTS.md`: prefer interpretable models for core pattern detection.

---

## 8) Known limitations (transparent)

- **Only linear trend:** slope assumes “roughly straight” direction; real businesses can be non-linear.
- **Period choice matters:** months 7–9 vs 10–12 is a business decision; can be parameterized.
- **Seasonality not handled here:** Trend detection is separate from seasonality decomposition.
- **Needs consistent history:** With fewer months, slope + MA become less reliable.

---

## 9) What we can improve next (optional talking points)

- Make “recent window” configurable (e.g., last 3 vs last 6 months).
- Add confidence / stability metrics (e.g., slope significance, volatility).
- Combine with seasonality/outlier checks to avoid mislabeling seasonal dips.
- Move from “month index” to real dates and support 24+ months seamlessly.

---

## 10) One-liner you can use in the meeting

“We detect trend using a simple, explainable model: **linear slope for long-term direction + recent 3-month vs previous 3-month momentum**, and we classify dealerships into Champion/Straggler/At Risk/Recovering based on those two signals.”

