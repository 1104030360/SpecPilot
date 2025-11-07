import json
from django.test import TestCase, Client


class APISpecificationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_generate_specification_success(self):
        data = {
            "user_id": 1,
            "order_id": 1,
            "spec_params": {"type": "A"}
        }
        response = self.client.post(
            "/polls/generate-specification/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["status"], "success")
        self.assertIsNone(result["error"])

    def test_generate_specification_missing_param(self):
        data = {"user_id": 1}
        response = self.client.post(
            "/polls/generate-specification/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertIsNotNone(result["error"])

    def test_generate_specification_invalid_param(self):
        data = {"user_id": 1, "order_id": 1, "spec_params": "not_a_dict"}
        response = self.client.post(
            "/polls/generate-specification/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertIsNotNone(result["error"])

    def test_retry_ai_success(self):
        data = {"task_id": 1}
        response = self.client.post(
            "/polls/retry-ai/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["status"], "success")
        self.assertIsNone(result["error"])

    def test_retry_ai_task_not_found(self):
        data = {"task_id": 999}
        response = self.client.post(
            "/polls/retry-ai/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        result = response.json()
        self.assertIsNotNone(result["error"])

    def test_retry_ai_service_error(self):
        data = {"task_id": -1}
        response = self.client.post(
            "/polls/retry-ai/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)
        result = response.json()
        self.assertIsNotNone(result["error"])
