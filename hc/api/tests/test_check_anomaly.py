from __future__ import annotations

from datetime import timedelta as td

from django.utils.timezone import now

from hc.api.models import Check, Ping
from hc.test import BaseTestCase


class CheckAnomalyTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.check = Check.objects.create(project=self.project, anomaly_enabled=True)
        self.url = f"/ping/{self.check.code}"

    def add_history(self, hours_since_last: float, count: int = 12) -> None:
        """Create daily pings, the most recent one hours_since_last hours ago."""
        t = now() - td(hours=hours_since_last)
        for i in range(count):
            Ping.objects.create(owner=self.check, created=t - td(hours=24 * i))

    def ping(self, url: str | None = None) -> None:
        r = self.client.get(url or self.url)
        self.assertEqual(r.status_code, 200)
        self.check.refresh_from_db()

    def test_regular_ping_is_not_flagged(self) -> None:
        self.add_history(24)
        self.ping()
        self.assertIsNone(self.check.last_anomaly)

    def test_late_ping_is_flagged(self) -> None:
        self.add_history(31)
        self.ping()
        self.assertIsNotNone(self.check.last_anomaly)

    def test_it_does_nothing_when_disabled(self) -> None:
        self.check.anomaly_enabled = False
        self.check.save()
        self.add_history(31)
        self.ping()
        self.assertIsNone(self.check.last_anomaly)

    def test_short_history_is_not_flagged(self) -> None:
        self.add_history(31, count=3)
        self.ping()
        self.assertIsNone(self.check.last_anomaly)

    def test_fail_ping_is_not_checked(self) -> None:
        self.add_history(31)
        self.ping(self.url + "/fail")
        self.assertIsNone(self.check.last_anomaly)

    def test_start_pings_are_left_out_of_history(self) -> None:
        self.add_history(24)
        Ping.objects.create(owner=self.check, kind="start", created=now() - td(hours=1))
        self.ping()
        self.assertIsNone(self.check.last_anomaly)

    def test_high_sensitivity_flags_smaller_change(self) -> None:
        self.add_history(24.6)
        self.ping()
        self.assertIsNone(self.check.last_anomaly)

        self.check.anomaly_sensitivity = "high"
        self.check.save()
        Ping.objects.filter(owner=self.check).delete()
        self.add_history(24.6)
        self.ping()
        self.assertIsNotNone(self.check.last_anomaly)
