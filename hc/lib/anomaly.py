"""Anomaly detection for ping intervals."""

from __future__ import annotations

from statistics import median

# The spread is never allowed to be smaller than this share of the usual interval.
MIN_SPREAD_RATIO = 0.01


def anomaly_score(history: list[float], new_interval: float) -> float:
    """Return how unusual new_interval is, compared with history."""
    middle = median(history)
    spread = median(abs(x - middle) for x in history)
    spread = max(spread, middle * MIN_SPREAD_RATIO)
    if spread == 0:
        return 0.0
    return abs(new_interval - middle) / spread


