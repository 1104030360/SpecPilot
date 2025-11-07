from django.test import TestCase
from django.urls import reverse
from polls.models import CategoryMemory
import json


class CategoryMemoryAPITest(TestCase):
    def setUp(self):
        self.list_url = reverse('category-memory-list')

    def test_create_valid_memory(self):
        data = {
            'configuration_item': 'Server A',
            'category': '伺服器問題'
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(
            CategoryMemory.objects.filter(
                configuration_item='Server A'
            ).exists()
        )

    def test_create_empty_config_item(self):
        data = {
            'configuration_item': '',
            'category': '測試分類'
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        error_msg = resp.json().get('error', '')
        self.assertIn('configuration_item', error_msg)

    def test_create_empty_category(self):
        data = {
            'configuration_item': 'Server B',
            'category': ''
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        error_msg = resp.json().get('error', '')
        self.assertIn('category', error_msg)

    def test_update_memory(self):
        memory = CategoryMemory.objects.create(
            configuration_item='Server C',
            category='舊分類'
        )
        url = reverse('category-memory-detail', args=[memory.id])
        data = {'category': '新分類'}
        resp = self.client.put(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        memory.refresh_from_db()
        self.assertEqual(memory.category, '新分類')

    def test_delete_memory(self):
        memory = CategoryMemory.objects.create(
            configuration_item='Server D',
            category='待刪除'
        )
        url = reverse('category-memory-detail', args=[memory.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            CategoryMemory.objects.filter(id=memory.id).exists()
        )

    def test_same_config_item_diff_categories(self):
        # 同一配置項可有多個不同分類記憶
        CategoryMemory.objects.create(
            configuration_item='Server E',
            category='分類A'
        )
        CategoryMemory.objects.create(
            configuration_item='Server E',
            category='分類B'
        )
        memories = CategoryMemory.objects.filter(
            configuration_item='Server E'
        )
        self.assertEqual(memories.count(), 2)

    def test_unique_together_constraint(self):
        # unique_together: 同一配置項+分類組合不可重複
        CategoryMemory.objects.create(
            configuration_item='Server F',
            category='重複分類'
        )
        data = {
            'configuration_item': 'Server F',
            'category': '重複分類'
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        # Django unique_together 會拋出 IntegrityError，API 應回傳 500
        self.assertEqual(resp.status_code, 500)
