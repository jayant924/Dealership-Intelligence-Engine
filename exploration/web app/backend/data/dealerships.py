"""
Dealership Data Source
======================
Single place for all raw dealership revenue data.

Later this can be replaced with:
  - CSV loader:   pd.read_csv("data/dealerships.csv")
  - JSON loader:  json.load(open("data/dealerships.json"))
  - DB query:     db.query("SELECT ...")
  - API call:     requests.get("https://dms-api/revenue")

All algorithms import from HERE — never define data inside algorithm files.
"""

# Each key = dealership name
# Each value = list of monthly revenue figures ($k), Jan → Dec
# Source: exploration/trend_detection_numpy_pandas.py

DEALERSHIPS: dict[str, list[float]] = {
    "champion":  [210, 215, 220, 218, 230, 235, 240, 238, 250, 255, 260, 265],
    "straggler": [280, 275, 268, 260, 255, 250, 248, 240, 235, 228, 220, 215],
}

# Month labels (1 = Jan, 12 = Dec)
MONTHS: list[int] = list(range(1, len(next(iter(DEALERSHIPS.values()))) + 1))
