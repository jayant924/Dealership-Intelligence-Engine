from fastapi import APIRouter, HTTPException

from algorithms.seasonality import get_all_seasonality, get_seasonality

router = APIRouter(prefix="/api/seasonality", tags=["seasonality"])


@router.get("/")
def all_seasonality():
    """Return seasonality decomposition for all dealerships."""
    return get_all_seasonality()


@router.get("/{dealership}")
def single_seasonality(dealership: str):
    """Return seasonality decomposition for a specific dealership."""
    try:
        return get_seasonality(dealership)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
