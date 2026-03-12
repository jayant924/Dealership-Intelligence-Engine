from fastapi import APIRouter, HTTPException

from algorithms.trend import get_all_trends, get_single_trend
from data.dealerships import DEALERSHIPS

router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.get("/")
def all_trends():
    """Return trend data for all dealerships."""
    return get_all_trends()


@router.get("/{dealership}")
def single_trend(dealership: str):
    """Return trend data for a specific dealership."""
    if dealership not in DEALERSHIPS:
        raise HTTPException(
            status_code=404,
            detail=f"Dealership '{dealership}' not found. "
                   f"Available: {list(DEALERSHIPS.keys())}",
        )
    return get_single_trend(dealership)
