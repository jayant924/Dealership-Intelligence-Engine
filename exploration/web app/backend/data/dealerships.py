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

# ── 1-YEAR DATA (Trend Detection) ────────────────────────────────────────────
# Each key = dealership name
# Each value = list of 12 monthly revenue figures ($k), Jan → Dec
# Source: exploration/trend_detection_numpy_pandas.py

DEALERSHIPS: dict[str, list[float]] = {
    "champion":  [210, 215, 220, 218, 230, 235, 240, 238, 250, 255, 260, 265],
    "straggler": [280, 275, 268, 260, 255, 250, 248, 240, 235, 228, 220, 215],
}

# Month labels (1 = Jan, 12 = Dec)
MONTHS: list[int] = list(range(1, len(next(iter(DEALERSHIPS.values()))) + 1))


# ── 3-YEAR DATA (Seasonality Detection) ──────────────────────────────────────
# 36 months (Jan 2021 → Dec 2023) — 3 years needed for period=12 decomposition.
# Built using: base trend + repeating seasonal pattern + random noise
# (Same approach as exploration/script/seasonality_detection.py)

DEALERSHIPS_3Y: dict[str, list[float]] = {
    # Growing dealership: upward trend (~210→300) with Oct/Nov festival spikes (+40/+60)
    "champion": [
        # 2021
        214.5, 214.1, 223.2, 216.7, 222.0, 226.5, 232.8, 227.9, 233.0, 277.2, 296.5, 237.6,
        # 2022
        240.1, 243.8, 247.5, 244.2, 251.0, 254.3, 258.1, 255.7, 261.3, 304.8, 325.1, 266.9,
        # 2023
        269.4, 272.1, 275.8, 273.0, 279.5, 283.2, 287.0, 284.6, 290.7, 334.5, 355.2, 296.3,
    ],
    # Declining dealership: downward trend (~280→200) with Oct/Nov festival spikes (+40/+60)
    "straggler": [
        # 2021
        283.1, 278.5, 272.0, 268.3, 261.9, 258.4, 255.7, 249.2, 244.6, 282.1, 301.8, 236.0,
        # 2022
        233.5, 229.8, 225.1, 221.6, 217.0, 213.5, 210.8, 206.3, 201.7, 240.2, 258.9, 193.2,
        # 2023
        190.7, 187.1, 183.4, 179.8, 175.2, 171.7, 168.9, 164.5, 160.0, 198.4, 217.1, 152.4,
    ],
}

MONTHS_3Y: list[int] = list(range(1, len(next(iter(DEALERSHIPS_3Y.values()))) + 1))
