# Learning: Trend and Seasonality Detection

This document provides a deep dive into the mathematical and conceptual foundations of Trend and Seasonality detection algorithms used within the JumpIQ Intelligence Engine.

---

## 1. Trend Detection

**What is it?** 
A trend represents a steady increase or decrease in a metric (e.g., Revenue, Valuation Score) over time.

**Mathematical Concepts:**

*   **Linear Regression (Slope):** We can plot our data points on a graph where the x-axis is time and the y-axis is the metric. Linear regression finds the "line of best fit" through these points. 
    *   If the slope of this line is positive (heading up), the trend is growing.
    *   If the slope is negative (heading down), the trend is declining.
*   **Moving Average:** This technique smooths out short-term fluctuations to highlight longer-term trends.
    *   *Calculation:* A 3-month moving average for April would be the average of sales in February, March, and April. By calculating this for every point, you get a smoother line that clearly shows direction without being distracted by day-to-day noise.

**Application in JumpIQ:**
*   **Quadrant Classification**: "Champions" have positive, sustained trends. "Stragglers" have negative trends.
*   **Opportunity Detection**: A dealership moving from a flat trend to a positive trend might be flagged as an "Opportunity."

---

## 2. Seasonality Detection

**What is it?**
Seasonality refers to predictable, recurring cycles or patterns over a specific timeframe (usually a year). 

**Mathematical Concepts:**

*   **Seasonal Decomposition:** This algorithm breaks down a time-series into three core components:
    1.  **Trend:** The overall direction (as discussed above).
    2.  **Seasonality:** The repeating cycle.
    3.  **Noise/Residual:** The random fluctuations left over after removing trend and seasonality.
*   **Prophet / ARIMA (SARIMA):** Advanced models that explicitly factor in specific dates. For example, Prophet can be told that "October" is a holiday month and will expect a spike, subtracting that expected spike before looking for anomalies in the remaining data.

**Application in JumpIQ:**
*   Dealership sales naturally spike during the festival season (e.g., October/November).
*   If we see a massive spike in October, the Seasonality detector tells the Super Agent: *"This is expected for this time of year; do not flag this as a rare, anomalous event."*
