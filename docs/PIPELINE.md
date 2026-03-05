# Data Pipeline — JumpIQ

The end-to-end flow from raw data to UI.

```
RAW DATA  →  Cleaning  →  Models  →  Derived Values  →  Rules  →  Database  →  UI
```

---

## Step 1 — Raw Data

**Sources:**

- DMS (Dealer Management System)
- Sales numbers
- Dealership financials
- Real estate valuation data

---

## Step 2 — Cleaning

Fix:

- Missing data
- Wrong values
- Duplicates

**Example:** `Jan revenue = null`  
**Approach:** Data imputation, e.g. `average(last 3 months)`.

---

## Step 3 — Models

Run algorithms for:

- Trend detection
- Seasonality detection
- Anomaly detection
- Forecasting

Dealership data is **time series** — values change over time, so time-series models are appropriate.

---

## Step 4 — Derived Values

New metrics computed from raw + cleaned + model outputs, e.g.:

- Valuation Score
- Profitability Score
- Momentum Score
- Market Health Score

---

## Step 5 — Rules

Business logic on derived values.

**Example:**

```
if revenue_growth > 20% and market_stable
  → mark as Opportunity
```

---

## Step 6 — Database

Store:

- Cleaned data
- Model outputs
- Derived values
- Rule outcomes

So UI and agents can query consistently.

---

## Step 7 — UI

Display:

- Revenue trend lines
- Momentum vs Environment
- Quadrant classification (Champions / Stragglers / Opportunities)
- Any anomaly flags and reasons

---

## Summary

| Stage           | Purpose                          |
|-----------------|-----------------------------------|
| Raw Data        | Ingest from DMS, sales, etc.     |
| Cleaning        | Imputation, validation, dedup    |
| Models          | Trend, seasonality, anomaly, forecast |
| Derived Values  | Scores (valuation, momentum, etc.) |
| Rules           | Classify (e.g. opportunity)       |
| Database        | Persist for UI and agents        |
| UI              | Dashboards and graphs            |
