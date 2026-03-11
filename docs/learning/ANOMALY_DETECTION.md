# Learning: Anomaly and Outlier Detection

This document covers the methods used to identify sudden, abnormal spikes or drops in data—known as outliers or anomalies.

---

## Outlier Detection Algorithms

An outlier is a data point that differs significantly from other observations. In JumpIQ, a sudden drop from 120 cars sold to 2 cars sold in a month is an outlier. The system must determine if this is a real business event or a data error.

### 1. Z-Score (Standardization)

**Concept:** The Z-score measures exactly how many standard deviations an element is from the mean of the dataset.

**Formulas:**
*   **Mean (μ):** The average of all data points.
*   **Standard Deviation (σ):** A measure of how spread out the numbers are.
*   **Z-Score (Z) = (X - μ) / σ** (where X is the specific data point).

**Rule of Thumb:** 
*   Generally, a Z-score greater than +3 or less than -3 indicates an anomaly. This means the point is extremely far from the average.

### 2. IQR (Interquartile Range)

**Concept:** IQR looks at the middle 50% of the data to find a "normal" range, and flags anything too far outside that box. It is often more robust than Z-Score because an extreme outlier won't skew the median as much as it skews the mean.

**Calculation:**
1.  Order the data from lowest to highest.
2.  Find **Q1** (the 25th percentile).
3.  Find **Q3** (the 75th percentile).
4.  Calculate **IQR = Q3 - Q1**.
5.  **Lower Bound:** Q1 - (1.5 * IQR)
6.  **Upper Bound:** Q3 + (1.5 * IQR)

**Rule of Thumb:**
*   Any data point falling below the Lower Bound or above the Upper Bound is flagged as an outlier.

### 3. Isolation Forest

**Concept:** A machine learning algorithm based on decision trees. It works by randomly selecting a feature and randomly selecting a split value. 
*   Because anomalies are rare and different, they are "isolated" much faster (closer to the root of the tree) than normal points.
*   *Note on usage:* While powerful, Isolation Forests are harder to "explain" to a user than Z-Score or IQR, which runs counter to our goal of highly interpretable reasons. Use sparingly when simpler methods fail.

---

## Application in JumpIQ

**The Outlier Agent:** When the Outlier Agent spots a massive Z-Score on a specific date, it alerts the Super Agent. The Super Agent can then cross-reference with the `Seasonality Agent` to ensure it wasn't just a predicted holiday spike, and if not, flag it for human review as a potential "Data Bug" or "Major Event."
