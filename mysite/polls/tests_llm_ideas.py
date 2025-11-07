"""
AI 想法衍生 API 測試
"""
import json
from django.test import TestCase, Client


class LLMIdeasAPITest(TestCase):
    """測試 AI 想法衍生 API"""

    def setUp(self):
        self.client = Client()
        self.url = '/polls/llm-ideas/'

    def test_method_not_allowed(self):
        """測試不允許的 HTTP 方法"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_missing_idea_parameter(self):
        """測試缺少想法參數"""
        response = self.client.post(
            self.url,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_empty_idea(self):
        """測試空白想法"""
        response = self.client.post(
            self.url,
            data=json.dumps({'idea': '   '}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_valid_idea_simple(self):
        """測試簡單想法"""
        response = self.client.post(
            self.url,
            data=json.dumps({'idea': '開發一個待辦事項應用'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertTrue(data['success'])
        self.assertIn('ideas', data)
        self.assertIsInstance(data['ideas'], list)
        self.assertGreater(len(data['ideas']), 0)
        self.assertLessEqual(len(data['ideas']), 3)

    def test_valid_idea_chinese(self):
        """測試中文想法"""
        response = self.client.post(
            self.url,
            data=json.dumps({'idea': '建立一個線上學習平台'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertTrue(data['success'])
        self.assertIn('ideas', data)
        self.assertIsInstance(data['ideas'], list)

    def test_valid_idea_english(self):
        """測試英文想法"""
        response = self.client.post(
            self.url,
            data=json.dumps({'idea': 'Build a social media platform'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertTrue(data['success'])
        self.assertIn('ideas', data)

    def test_complex_idea(self):
        """測試複雜想法"""
        complex_idea = """
        我想開發一個整合 AI 的智慧家居系統，
        能夠學習使用者的習慣，自動調整溫度、
        照明和安全設定。
        """
        response = self.client.post(
            self.url,
            data=json.dumps({'idea': complex_idea}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertTrue(data['success'])
        self.assertIn('ideas', data)
        self.assertGreater(len(data['ideas']), 0)

    def test_response_structure(self):
        """測試回應結構"""
        response = self.client.post(
            self.url,
            data=json.dumps({'idea': '開發一個健康追蹤 App'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # 檢查必要欄位
        self.assertIn('success', data)
        self.assertIn('ideas', data)
        
        # 檢查想法是字串列表
        for idea in data['ideas']:
            self.assertIsInstance(idea, str)
            self.assertGreater(len(idea), 0)

    def test_invalid_json(self):
        """測試無效的 JSON"""
        response = self.client.post(
            self.url,
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_special_characters(self):
        """測試特殊字符"""
        response = self.client.post(
            self.url,
            data=json.dumps({
                'idea': '開發一個支援 @#$%^&* 特殊符號的系統'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_long_idea(self):
        """測試長篇想法"""
        long_idea = '開發一個系統 ' * 100  # 重複100次
        response = self.client.post(
            self.url,
            data=json.dumps({'idea': long_idea}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
