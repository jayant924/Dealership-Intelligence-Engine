# Pattern Detection — What to Detect and How

Different algorithms detect different patterns. This doc maps **pattern types** to **methods**.

---

## 1. Trend

**What:** Revenue (or other metric) increasing or decreasing steadily over time.

**Ideas:**

- Linear regression (slope)
- Slope detection over windows
- Moving average to smooth and then assess direction

**Use case:** “Is this dealership on an upward or downward trajectory?”

---

## 2. Seasonality

**What:** Recurring cycles (e.g. same months every year spike or dip).

**Example:** Car sales increase in Oct/Nov (festivals).

**Algorithms / tools:**

- Seasonal decomposition (e.g. `statsmodels.tsa.seasonal.seasonal_decompose`)
- Prophet (Facebook) — built-in seasonality
- ARIMA (seasonal component)

**Use case:** “Is this spike normal for this time of year?”

---

## 3. Outliers

**What:** Single points (or short windows) that are abnormally high or low.

**Example:** Sales drop from 120 cars to 2 cars in one month.

**Possible causes:** Data bug, one-off business issue, reporting error.

**Algorithms:**

- **Z-score** — how many standard deviations from mean
- **IQR** (Interquartile Range) — flag outside 1.5× IQR
- **Isolation Forest** — tree-based anomaly score (use with care for interpretability)

**Use case:** “Is this point real or a data error?”

---

## 4. Event Impact

**What:** Impact of one-off or external events (economic crash, fuel price spike, policy change).

**Approach:** Often needs:

- Event labels (dates + type)
- Before/after comparison
- Or causal / impact models

**Use case:** “Why did revenue change in this period?”

---

## Summary Table

| Pattern       | Example                    | Algorithms / Tools                    |
|---------------|----------------------------|----------------------------------------|
| Trend         | Steady growth/decline      | Linear regression, slope, moving avg   |
| Seasonality   | Recurring cycles           | Seasonal decomp, Prophet, ARIMA        |
| Outliers      | Sudden spike/drop          | Z-score, IQR, Isolation Forest         |
| Event impact  | One-off external event     | Event dates, before/after, causal      |

---

## Interpretability

Prefer **interpretable** methods so the system can explain:

- “Revenue dropped because …”
- “Spike is consistent with seasonal pattern.”
- “This point is an outlier; possible data issue.”

Neural networks are discouraged for this reason (“black box”). Use regression, statistical rules, and classical time-series models where possible.
