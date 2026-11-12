from __future__ import annotations

from unittest import TestCase

from hc.lib.anomaly import anomaly_score

HISTORY = [24, 25, 23, 26, 24, 22, 25, 23, 26, 24]


class AnomalyScoreTestCase(TestCase):
    def test_far_interval_scores_high(self) -> None:
        self.assertEqual(anomaly_score(HISTORY, 31), 7.0)

    def test_close_interval_scores_low(self) -> None:
        self.assertEqual(anomaly_score(HISTORY, 25), 1.0)

    def test_identical_history_does_not_crash(self) -> None:
        score = anomaly_score([24, 24, 24, 24, 24], 31)
        self.assertGreater(score, 3)


