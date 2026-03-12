# Seasonality Detection Explained — Beginner's Guide

**Source code:** [exploration/script/seasonality_detection.py](../../exploration/script/seasonality_detection.py) (standalone script) | [exploration/web app/backend/algorithms/seasonality.py](../../exploration/web%20app/backend/algorithms/seasonality.py) (API version)

Now that we understand **Trend Detection** ([trend_detection.md](trend_detection.md)) — which tells us the general direction a dealership is heading — we need to tackle the next big challenge: **Seasonality**.

Let's use the same data we started with, but add a real-world twist to it.

---

## 1. The Problem — Why Trend Detection Isn't Enough

Imagine it's November. You look at your "Champion" dealership's sales:

```python
# Normal Champion Data:
# [210, 215, 220, 218, 230, 235, 240, 238, 250, 255, 260, 265]
```

But in the real world, October and November are **festival season**. Dealerships always sell way more cars during this time. So the *actual* data looks like this:

```python
df = pd.DataFrame({
    "month":     list(range(1, 13)),
    "champion":  [210, 215, 220, 218, 230, 235, 240, 238, 250, 295, 300, 265] 
    # Notice months 10 & 11 (Oct/Nov):     Normal (~255, 260)  -->  Spiked (295, 300)
})
```

If we just use simple math, a basic system might scream: **"URGENT: MASSIVE UNEXPECTED SPIKE IN SALES IN NOV! AND THEN A MASSIVE DROP IN DEC!"**

But as a human, you know this isn't an anomaly. It's just a festival. It happens every year.
**Seasonality Detection finds these repeating patterns so we don't accidentally flag them as anomalies.**

---

## 2. The Core Concept — Breaking the Line into 3 Pieces

In data science, we believe that any time-series data (like monthly sales) is actually three different lines stacked on top of each other:

`Total Sales = Trend + Seasonality + Residual`

1. **Trend:** The baseline trajectory (e.g., growing by 5 cars a month).
2. **Seasonal:** The expected calendar effect (e.g., "+40 cars every November").
3. **Residual (Noise):** The *actual* unexpected surprise (e.g., "+5 cars because it was sunny that weekend").

### How do we separate them?

We use a statistical algorithm called **Seasonal Decomposition** (specifically, `seasonal_decompose` from the `statsmodels` library).

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# We ask the algorithm to break down our Champion's sales
# period=12 tells it: "Look for patterns that repeat every 12 months"
result = seasonal_decompose(df['champion'], model='additive', period=12)
```

---

## 3. What the Algorithm Outputs

When you run that code, `result` gives you three separate lists of numbers. Let's look at what the algorithm says about our **November (Month 11)** spike where sales hit **300**.

### A. The Underling Trend (`result.trend`)
The algorithm figures out the long-term slope, ignoring the spikes.
It says: *"If there was no festival, the baseline trend predicts they would have sold **260** cars in November."*

### B. The Seasonal Component (`result.seasonal`)
The algorithm looks at historical data and notices a repeating pattern.
It says: *"Historically, November always brings an extra **+40** cars compared to the baseline, due to festivals."*

### C. The Residual/Noise (`result.resid`)
This is the most important part. To find the leftover "surprise", the algorithm subtracts the expected Trend and Seasonality from the raw total:

**Formula:**
`Residual = Total Sales - (Baseline Trend + Expected Seasonal Spike)`
`Residual = 300 - (260 + 40)`
`Residual = 0`

**Conclusion for November:**
The residual is exactly 0. Even though 300 cars is their highest month ever, the algorithm knows it is **100% normal and expected**. No anomaly alarm is triggered!

---

## 4. Why This Matters for the "Super Agent"

Let's look at **March (Month 3)**. Sales were **220**.

Let's say hypothetically, the dealership threw a massive marketing event in March that unexpected failed. Sales plummeted to **180**.

**How the agents see it:**
1. **Raw data:** 180 cars.
2. **Trend expectation:** 220 cars.
3. **Seasonal expectation for March:** 0 cars (March is usually a boring, average month).
4. **Residual Calculation:** `180 - (220 + 0) = -40`

The **Residual is -40**. The system expected 220, but got 180.
Because the Residual is a large negative number, the system realizes this is a genuine, unexpected problem.

### The Pipeline:
1. The **Trend Agent** establishes the baseline.
2. The **Seasonality Agent** strips away the expected festive spikes.
3. The **Outlier Agent** only looks at the *Residuals* to find real problems.

By extracting the Seasonality, our Outlier Agent becomes incredibly smart. It stops panicking over December drops (post-festival cooldowns) and starts catching real issues (like a bad marketing campaign in March).
