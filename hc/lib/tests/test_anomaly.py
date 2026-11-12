from __future__ import annotations

from unittest import TestCase

from hc.lib.anomaly import anomaly_score, is_anomalous

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


