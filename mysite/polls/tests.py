

from django.test import TestCase, Client
from django.urls import reverse


class APITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_generate_specification_success(self):
        url = reverse('generate_specification_api')
        data = {
            'user_id': 1,
            'order_id': 1,
            'spec_params': {
                'project_goal': '打造智慧客服系統',
                'core_features': '自動回覆、語音辨識',
            }
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'success')

    def test_generate_specification_missing_fields(self):
        url = reverse('generate_specification_api')
        data = {
            'user_id': 1,
            'order_id': 1,
            'spec_params': {
                'project_goal': '',
                'core_features': '',
            }
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'success')

    def test_generate_specification_method_not_allowed(self):
        url = reverse('generate_specification_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())

    def test_retry_ai_success(self):
        url = reverse('retry_ai_api')
        data = {'task_id': 1}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'success')

    def test_retry_ai_method_not_allowed(self):
        url = reverse('retry_ai_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())


class SpecGeneratorViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('spec_generator')

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI 規格產生器')

    def test_post_all_fields(self):
        data = {
            'project_goal': '打造智慧客服系統',
            'core_features': '自動回覆、語音辨識',
            'technical_constraints': 'Python, Django',
            'target_audience': '企業用戶',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '打造智慧客服系統')
        self.assertContains(response, '自動回覆')
        self.assertContains(response, 'Python')
        self.assertContains(response, '企業用戶')
        self.assertContains(response, '背景說明')
        self.assertContains(response, '目標：打造智慧客服系統')
        self.assertContains(response, '功能規格：自動回覆、語音辨識')

    def test_post_missing_fields(self):
        data = {
            'project_goal': '',
            'core_features': '',
            'technical_constraints': '',
            'target_audience': '',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '背景說明')
