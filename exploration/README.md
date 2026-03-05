# Exploration — Phase 1

**Before coding:** Read [../docs/EXPLORATION-PRINCIPLES.md](../docs/EXPLORATION-PRINCIPLES.md). Understand → Analyze → Explain → Then Implement. Relate every concept to JumpIQ.

Place for notebooks and scripts while learning:

- **Trend detection** (slope, moving average)
- **Seasonality** (decomposition, Prophet, ARIMA)
- **Outlier detection** (Z-score, IQR, Isolation Forest)
- **Time series forecasting** (ARIMA, Prophet)

See [../docs/PHASE1-STUDY.md](../docs/PHASE1-STUDY.md) for what to study and in what order.

Suggested structure as you go:

```
exploration/
├── 01_trend_slope_moving_avg.ipynb   # or .py
├── 02_outliers_zscore_iqr.ipynb
├── 03_seasonality_decomposition.ipynb
├── 04_forecasting_arima_prophet.ipynb
└── README.md
```

Run from project root:

```bash
pip install -r requirements.txt
# Optional: jupyter lab  or  jupyter notebook
```
