"""
JumpIQ — Dealership Intelligence Engine
FastAPI Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import trends, seasonality

app = FastAPI(
    title="JumpIQ Intelligence Engine",
    description="Trend and Seasonality analysis for dealership revenue data",
    version="0.1.0",
)

# Allow Angular dev server (localhost:4200)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(trends.router)
app.include_router(seasonality.router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "endpoints": [
            "/api/trends",
            "/api/trends/{dealership}",
            "/api/seasonality",
            "/api/seasonality/{dealership}",
        ],
    }
