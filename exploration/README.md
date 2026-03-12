# Exploration — Phase 1

**Before coding:** Read [../docs/EXPLORATION-PRINCIPLES.md](../docs/EXPLORATION-PRINCIPLES.md). Understand → Analyze → Explain → Then Implement. Relate every concept to JumpIQ.

Place for notebooks, scripts, and the working PoC web app built during learning.

---

## Structure

```
exploration/
├── README.md                       # This file
├── script/                         # Standalone learning scripts
│   ├── trend_detection.py          # Slope, moving average, period comparison, classification
│   └── seasonality_detection.py    # Seasonal decomposition, residuals, anomaly demo
└── web app/                        # Working PoC dashboard (FastAPI + Angular)
    ├── backend/                    # Python API server
    │   ├── main.py                 # FastAPI app, CORS, routers
    │   ├── requirements.txt        # Backend dependencies
    │   ├── data/
    │   │   └── dealerships.py      # Single data source (DEALERSHIPS dict, MONTHS list)
    │   ├── algorithms/
    │   │   ├── trend.py            # Trend detection (slope, trend line, MA, classify)
    │   │   └── seasonality.py      # Seasonality decomposition (statsmodels)
    │   └── routers/
    │       ├── trends.py           # GET /api/trends/, /api/trends/{dealership}
    │       └── seasonality.py      # GET /api/seasonality/, /api/seasonality/{dealership}
    └── frontend/                   # Angular 21 + ECharts dashboard
        └── src/app/
            ├── app.ts              # Root component
            ├── app.config.ts       # Providers (zone.js, HttpClient)
            ├── services/
            │   └── intelligence.service.ts   # HTTP calls + TypeScript interfaces
            ├── dashboard/
            │   ├── dashboard.component.ts    # Main dashboard (cards + charts)
            │   ├── dashboard.component.html  # Template
            │   └── dashboard.component.scss  # Styles
            └── charts/
                ├── trend-chart.component.ts        # Revenue trend chart (ECharts)
                └── seasonality-chart.component.ts  # Seasonality decomposition chart
```

---

## Topics Covered

- **Trend detection** — slope, moving average, period comparison, quadrant classification
- **Seasonality** — additive decomposition (observed / trend / seasonal / residual)
- **Outlier detection** — Z-score, IQR, Isolation Forest (see [../docs/learning/ANOMALY_DETECTION.md](../docs/learning/ANOMALY_DETECTION.md))
- **Time series forecasting** — ARIMA, Prophet (planned)

See [../docs/PHASE1-STUDY.md](../docs/PHASE1-STUDY.md) for what to study and in what order.

---

## Running the Scripts

```bash
# From project root
pip install -r requirements.txt

# Run standalone scripts
python exploration/script/trend_detection.py
python exploration/script/seasonality_detection.py
```

---

## Running the Web App

```bash
# Backend
cd exploration/web\ app/backend
pip install -r requirements.txt
uvicorn main:app --reload          # → http://localhost:8000

# Frontend (separate terminal)
cd exploration/web\ app/frontend
npm install
npx ng serve                       # → http://localhost:4200
```

---

## Algorithm Documentation

Detailed beginner-friendly explanations of each algorithm:

- [Trend Detection Guide](../docs/algorithms/trend_detection.md) — slope, moving average, period comparison, quadrant classification
- [Seasonality Detection Guide](../docs/algorithms/seasonality_detection.md) — seasonal decomposition, residuals, how agents use it
- [Anomaly Detection Learning](../docs/learning/ANOMALY_DETECTION.md) — Z-score, IQR, Isolation Forest
- [Trend & Seasonality Learning](../docs/learning/TREND_AND_SEASONALITY.md) — mathematical foundations
