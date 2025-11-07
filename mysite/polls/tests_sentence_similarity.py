import json
from django.test import TestCase, Client
from django.urls import reverse


class SentenceSimilarityAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('sentence_similarity_api')

    def test_similarity_identical_sentences(self):
        """測試相同句子的相似度"""
        data = {
            'sentence1': 'hello world',
            'sentence2': 'hello world'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['similarity'], 1.0)
        self.assertTrue(result['is_similar'])

    def test_similarity_different_sentences(self):
        """測試完全不同句子的相似度"""
        data = {
            'sentence1': 'hello world',
            'sentence2': 'goodbye universe'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertLess(result['similarity'], 0.5)
        self.assertFalse(result['is_similar'])

    def test_similarity_partial_overlap(self):
        """測試部分重疊句子的相似度"""
        data = {
            'sentence1': 'hello beautiful world',
            'sentence2': 'hello wonderful world'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertGreaterEqual(result['similarity'], 0.5)

    def test_similarity_missing_sentence(self):
        """測試缺少句子參數"""
        data = {
            'sentence1': 'hello world'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertIn('error', result)

    def test_similarity_empty_sentences(self):
        """測試空句子"""
        data = {
            'sentence1': '',
            'sentence2': ''
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_similarity_custom_threshold(self):
        """測試自訂相似度門檻"""
        data = {
            'sentence1': 'hello world',
            'sentence2': 'hello earth',
            'threshold': 0.5
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['threshold'], 0.5)
        self.assertIn('is_similar', result)

    def test_similarity_method_not_allowed(self):
        """測試不允許的 HTTP 方法"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        result = response.json()
        self.assertIn('error', result)

    def test_similarity_chinese_sentences(self):
        """測試中文句子相似度"""
        data = {
            'sentence1': '今天天氣很好',
            'sentence2': '今天天氣不錯'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('similarity', result)
        self.assertGreaterEqual(result['similarity'], 0.0)
        self.assertLessEqual(result['similarity'], 1.0)
