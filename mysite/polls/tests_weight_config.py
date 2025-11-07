from django.test import TestCase, Client
from django.urls import reverse
import json

class WeightConfigTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('weight_config_list')

    def test_create_valid_config(self):
        data = {
            'name': 'default',
            'score_a': 0.4,
            'score_b': 0.3,
            'score_c': 0.2,
            'score_d': 0.1,
        }
        response = self.client.post(self.list_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.json())
        self.assertEqual(response.json()['result'], 'created')

    def test_create_invalid_total(self):
        data = {
            'name': 'invalid',
            'score_a': 0.5,
            'score_b': 0.5,
            'score_c': 0.2,
            'score_d': 0.1,
        }
        response = self.client.post(self.list_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn('分數總和必須等於 1.0', response.json()['error'])

    def test_create_invalid_range(self):
        data = {
            'name': 'invalid2',
            'score_a': 1.2,
            'score_b': -0.1,
            'score_c': 0.5,
            'score_d': -0.6,
        }
        response = self.client.post(self.list_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn('所有分數必須介於 0~1 之間', response.json()['error'])

    def test_list_configs(self):
        # 先建立一筆
        data = {
            'name': 'default',
            'score_a': 0.25,
            'score_b': 0.25,
            'score_c': 0.25,
            'score_d': 0.25,
        }
        self.client.post(self.list_url, json.dumps(data), content_type='application/json')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('configs', response.json())
        self.assertGreaterEqual(len(response.json()['configs']), 1)

    def test_update_config(self):
        # 建立
        data = {
            'name': 'update',
            'score_a': 0.25,
            'score_b': 0.25,
            'score_c': 0.25,
            'score_d': 0.25,
        }
        create_resp = self.client.post(self.list_url, json.dumps(data), content_type='application/json')
        config_id = create_resp.json()['id']
        url = reverse('weight_config_detail', args=[config_id])
        update_data = {
            'name': 'updated',
            'score_a': 0.1,
            'score_b': 0.2,
            'score_c': 0.3,
            'score_d': 0.4,
        }
        resp = self.client.put(url, json.dumps(update_data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('result', resp.json())
        self.assertEqual(resp.json()['result'], 'updated')

    def test_delete_config(self):
        # 建立
        data = {
            'name': 'delete',
            'score_a': 0.25,
            'score_b': 0.25,
            'score_c': 0.25,
            'score_d': 0.25,
        }
        create_resp = self.client.post(self.list_url, json.dumps(data), content_type='application/json')
        config_id = create_resp.json()['id']
        url = reverse('weight_config_detail', args=[config_id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('result', resp.json())
        self.assertEqual(resp.json()['result'], 'deleted')
