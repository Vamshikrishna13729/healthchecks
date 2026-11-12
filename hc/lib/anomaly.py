"""Anomaly detection for ping intervals."""

from __future__ import annotations

from statistics import median

# The spread is never allowed to be smaller than this share of the usual interval.
MIN_SPREAD_RATIO = 0.01

MIN_HISTORY = 10

THRESHOLDS = {"low": 4.0, "medium": 3.0, "high": 2.0}
def anomaly_score(history: list[float], new_interval: float) -> float:
    """Return how unusual new_interval is, compared with history."""
    middle = median(history)
    spread = median(abs(x - middle) for x in history)
    spread = max(spread, middle * MIN_SPREAD_RATIO)
# Scoring starts only after this many intervals are recorded.
    

# A score above the threshold is anomalous. Higher sensitivity means a lower threshold.
    
    if spread == 0:
        return 0.0
    return abs(new_interval - middle) / spread


def is_anomalous(
    history: list[float], new_interval: float, sensitivity: str = "medium"
) -> bool:
    """Return True if new_interval is unusual for this history."""
    if len(history) < MIN_HISTORY:
        return False
    return anomaly_score(history, new_interval) > THRESHOLDS[sensitivity]


