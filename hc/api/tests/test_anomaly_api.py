from __future__ import annotations

from typing import Any

from hc.api.models import Check
from hc.test import BaseTestCase, TestHttpResponse


class AnomalyApiTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.check = Check.objects.create(project=self.project)
        self.url = f"/api/v3/checks/{self.check.code}"

    def post(self, url: str, data: dict[str, Any]) -> TestHttpResponse:
        return self.client.post(
            url, data, content_type="application/json", HTTP_X_API_KEY="X" * 32
        )

    def test_output_has_anomaly_fields(self) -> None:
        r = self.client.get(self.url, HTTP_X_API_KEY="X" * 32)
        self.assertEqual(r.status_code, 200)
        doc = r.json()
        self.assertEqual(doc["anomaly_enabled"], False)
        self.assertEqual(doc["anomaly_sensitivity"], "medium")
        self.assertIsNone(doc["last_anomaly"])

    def test_it_updates_settings(self) -> None:
        r = self.post(self.url, {"anomaly_enabled": True, "anomaly_sensitivity": "high"})
        self.assertEqual(r.status_code, 200)
        self.check.refresh_from_db()
        self.assertTrue(self.check.anomaly_enabled)
        self.assertEqual(self.check.anomaly_sensitivity, "high")

    def test_it_creates_check_with_settings(self) -> None:
        r = self.post("/api/v3/checks/", {"name": "Backup", "anomaly_enabled": True})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["anomaly_enabled"], True)

    def test_it_rejects_unknown_sensitivity(self) -> None:
        r = self.post(self.url, {"anomaly_sensitivity": "extreme"})
        self.assertEqual(r.status_code, 400)

    def test_it_rejects_non_boolean_enabled(self) -> None:
        r = self.post(self.url, {"anomaly_enabled": "yes"})
        self.assertEqual(r.status_code, 400)

    def test_other_updates_leave_settings_alone(self) -> None:
        self.check.anomaly_enabled = True
        self.check.save()
        r = self.post(self.url, {"name": "Renamed"})
        self.assertEqual(r.status_code, 200)
        self.check.refresh_from_db()
        self.assertTrue(self.check.anomaly_enabled)
