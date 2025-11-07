import json
from django.test import TestCase, Client
from polls.models import FieldPriorityConfiguration


class FieldPriorityConfigurationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_field_priority_config(self):
        data = {
            "name": "預設欄位順序",
            "field_order": ["name", "email", "phone"]
        }
        response = self.client.post(
            "/polls/field-priority/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["result"], "created")

    def test_field_priority_invalid_format(self):
        data = {
            "name": "錯誤格式",
            "field_order": "not_a_list"
        }
        response = self.client.post(
            "/polls/field-priority/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertIsNotNone(result["error"])

    def test_get_field_priority_list(self):
        FieldPriorityConfiguration.objects.create(
            name="測試配置",
            field_order=["a", "b", "c"]
        )
        response = self.client.get("/polls/field-priority/")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(len(result["configs"]), 1)

    def test_update_field_priority_config(self):
        config = FieldPriorityConfiguration.objects.create(
            name="測試",
            field_order=["a", "b"]
        )
        data = {"field_order": ["c", "d", "e"]}
        response = self.client.put(
            f"/polls/field-priority/{config.id}/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        config.refresh_from_db()
        self.assertEqual(config.field_order, ["c", "d", "e"])

    def test_delete_field_priority_config(self):
        config = FieldPriorityConfiguration.objects.create(
            name="刪除測試",
            field_order=["x"]
        )
        response = self.client.delete(f"/polls/field-priority/{config.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            FieldPriorityConfiguration.objects.filter(id=config.id).exists()
        )
