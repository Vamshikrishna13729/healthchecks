from __future__ import annotations

from datetime import datetime

from unittest import TestCase

from hc.lib.anomaly import anomaly_score, intervals, is_anomalous

HISTORY = [24, 25, 23, 26, 24, 22, 25, 23, 26, 24]


class AnomalyScoreTestCase(TestCase):
    def test_far_interval_scores_high(self) -> None:
        self.assertEqual(anomaly_score(HISTORY, 31), 7.0)

    def test_close_interval_scores_low(self) -> None:
        self.assertEqual(anomaly_score(HISTORY, 25), 1.0)

    def test_identical_history_does_not_crash(self) -> None:
        score = anomaly_score([24, 24, 24, 24, 24], 31)
        self.assertGreater(score, 3)


class IsAnomalousTestCase(TestCase):
    def test_far_interval_is_anomalous(self) -> None:
        self.assertTrue(is_anomalous(HISTORY, 31))

    def test_close_interval_is_normal(self) -> None:
        self.assertFalse(is_anomalous(HISTORY, 25))

    def test_high_sensitivity_flags_smaller_change(self) -> None:
        self.assertFalse(is_anomalous(HISTORY, 26.5, "medium"))
        self.assertTrue(is_anomalous(HISTORY, 26.5, "high"))
    def test_short_history_is_never_anomalous(self) -> None:
        self.assertFalse(is_anomalous([24, 24, 24], 100))


class IntervalsTestCase(TestCase):
    def test_it_returns_seconds_between_pings(self) -> None:
        times = [
            datetime(2026, 11, 9, 2, 0),
            datetime(2026, 11, 9, 2, 30),
            datetime(2026, 11, 9, 3, 30),
        ]
        self.assertEqual(intervals(times), [1800.0, 3600.0])

    def test_it_sorts_the_timestamps_first(self) -> None:
        times = [datetime(2026, 11, 9, 2, 30), datetime(2026, 11, 9, 2, 0)]
        self.assertEqual(intervals(times), [1800.0])

    def test_one_ping_gives_no_interval(self) -> None:
        self.assertEqual(intervals([datetime(2026, 11, 9, 2, 0)]), [])


