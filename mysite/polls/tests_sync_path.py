from django.test import TestCase
from django.urls import reverse
from polls.models import SyncPathConfiguration
import os
import tempfile
import json

class SyncPathConfigurationAPITest(TestCase):
    def setUp(self):
        self.valid_path = tempfile.mkdtemp()
        self.invalid_path = '/root/invalid_path_xyz'
        self.api_url = reverse('sync-path-list')

    def tearDown(self):
        if os.path.exists(self.valid_path):
            try:
                os.rmdir(self.valid_path)
            except Exception:
                pass

    def test_create_valid_path(self):
        data = {'name': 'test', 'path': self.valid_path}
        resp = self.client.post(
            self.api_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(
            SyncPathConfiguration.objects.filter(name='test').exists()
        )

    def test_create_invalid_path(self):
        data = {'name': 'bad', 'path': self.invalid_path}
        resp = self.client.post(
            self.api_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        error_msg = resp.json().get('error', '')
        # 無效路徑可能是「不存在」或「不可寫入」
        self.assertTrue(
            '路徑不存在' in error_msg or '不可寫入' in error_msg
        )

    def test_update_path(self):
        obj = SyncPathConfiguration.objects.create(
            name='update', path=self.valid_path
        )
        new_path = tempfile.mkdtemp()
        url = reverse('sync-path-detail', args=[obj.id])
        data = {'name': 'update', 'path': new_path}
        resp = self.client.put(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        obj.refresh_from_db()
        self.assertEqual(obj.path, new_path)
        if os.path.exists(new_path):
            try:
                os.rmdir(new_path)
            except Exception:
                pass

    def test_delete_path(self):
        obj = SyncPathConfiguration.objects.create(
            name='delete', path=self.valid_path
        )
        url = reverse('sync-path-detail', args=[obj.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            SyncPathConfiguration.objects.filter(id=obj.id).exists()
        )

    def test_path_format_validation(self):
        data = {'name': 'format', 'path': ''}
        resp = self.client.post(
            self.api_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        error_msg = resp.json().get('error', '')
        self.assertIn('path 必須為非空字串', error_msg)
