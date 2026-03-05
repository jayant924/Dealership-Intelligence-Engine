# Phase 1 — What to Study First

**Goal:** Understand algorithms deeply (pattern detection, time-series analysis, anomaly detection). Not just run code — know *why* and *when* each method applies.

**Before you start:** Read [EXPLORATION-PRINCIPLES.md](EXPLORATION-PRINCIPLES.md). Do not jump to coding; understand pattern → algorithm → result → explanation. Relate every concept to JumpIQ dealership data.

Deliverable: **Daily report** (what you studied + how it applies to dealership revenue).

---

## 1. Trend Detection

**Concepts:**

- Slope calculation (e.g. linear regression on time index)
- Moving average (smoothing, then direction)
- Comparing periods (e.g. last 3 months vs previous 3 months)

**Practice:**

- Implement or use slope on a simple time series.
- Compare moving average vs raw series.

**How this applies to JumpIQ:** Revenue and valuation are time-based. Trend (slope, moving average) answers: *Is this dealership’s revenue/valuation going up or down over time?* Needed for quadrant classification (Champions vs Stragglers) and opportunity detection.

---

## 2. Seasonality Detection

**Concepts:**

- Seasonal decomposition (trend + seasonal + residual)
- Prophet (additive seasonality, holidays)
- ARIMA (including seasonal ARIMA — SARIMA)

**Practice:**

- Decompose a series with clear seasonality (e.g. monthly car sales).
- Use Prophet or SARIMA on the same series; interpret components.

**How this applies to JumpIQ:** Dealership sales spike in Oct–Nov (festivals). Seasonality detection tells us *is this spike normal for this time of year?* so we don’t wrongly flag a seasonal bump as an anomaly or opportunity.

---

## 3. Outlier Detection

**Concepts:**

- **Z-score:** `(x - mean) / std`; flag if |z| > 2 or 3.
- **IQR:** Q1, Q3, IQR = Q3−Q1; flag if x < Q1−1.5×IQR or x > Q3+1.5×IQR.
- **Isolation Forest:** sklearn `IsolationForest` — understand what it does and how to interpret.

**Practice:**

- Add an artificial outlier to a series; detect it with Z-score and IQR.
- Compare with Isolation Forest; note interpretability trade-off.

**How this applies to JumpIQ:** Sudden drop (e.g. 100 cars → 2 cars) could be data bug, API issue, or real problem. Outlier detection triggers investigation; Z-score/IQR are interpretable (“this point is 4 std away from mean”).

---

## 4. Time Series Forecasting

**Concepts:**

- **ARIMA:** AutoRegressive Integrated Moving Average (order p, d, q).
- **Prophet:** Trend + seasonality + holidays; good for business series.
- **Simple baselines:** last value, moving average.

**Practice:**

- Fit ARIMA and Prophet on a small dataset.
- Compare forecasts and interpret (trend vs seasonal).

**How this applies to JumpIQ:** Forecasting supports “what happens next?” for revenue/valuation and helps set expectations. When actual deviates from forecast, that can trigger anomaly investigation. Use interpretable methods so we can explain.

---

## Suggested Order

1. **Trend** (slope, moving average) — simplest.
2. **Outliers** (Z-score, IQR) — no forecasting needed.
3. **Seasonality** (decomposition, then Prophet/ARIMA).
4. **Forecasting** (ARIMA, Prophet) — builds on trend + seasonality.

---

## Tech Stack

- **Python**
- **Pandas** — series, dates, grouping
- **NumPy** — basic stats (mean, std, percentiles)
- **statsmodels** — decomposition, ARIMA
- **prophet** (optional) — Prophet
- **scikit-learn** — Isolation Forest, regression

---

## Daily Report Format

Your senior asked for daily reports that prove **real understanding**. Include:

1. **Today I studied:** e.g. trend detection, slope calculation, moving average.
2. **How it applies to dealership revenue:** one or two sentences tying the concept to JumpIQ (e.g. “Slope tells us if revenue is improving or declining over time; we need this for Champions vs Stragglers.”).
3. **Tomorrow I will:** one concrete next step.

Keep it short and consistent; focus on depth of understanding, not quantity. Do not report “I coded X” without “I understand how/why/when it works.”
