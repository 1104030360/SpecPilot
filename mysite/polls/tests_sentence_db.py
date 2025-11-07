from django.test import TestCase, Client
from django.urls import reverse
from polls.models import SentenceDatabase
import json

class SentenceDatabaseAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('sentence_db_list')
        self.sim_url = reverse('sentence_similarity_api')
        self.item = SentenceDatabase.objects.create(
            user='user1', sentence='你好世界', category='greet', embedding=[0.1, 0.2, 0.3]
        )

    def test_create_sentence(self):
        payload = {
            'user': 'user2',
            'sentence': '早安',
            'category': 'greet',
            'embedding': [0.2, 0.1, 0.3]
        }
        resp = self.client.post(self.list_url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('id', resp.json())

    def test_get_sentence_list(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('sentences', resp.json())
        self.assertGreaterEqual(len(resp.json()['sentences']), 1)

    def test_update_sentence(self):
        url = reverse('sentence_db_detail', args=[self.item.id])
        payload = {'sentence': '世界你好'}
        resp = self.client.put(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.sentence, '世界你好')

    def test_delete_sentence(self):
        url = reverse('sentence_db_detail', args=[self.item.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(SentenceDatabase.objects.filter(id=self.item.id).exists())

    def test_similarity_stub(self):
        payload = {'sentence1': '你好', 'sentence2': '早安'}
        resp = self.client.post(self.sim_url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('similarity', resp.json())
        self.assertEqual(resp.json()['similarity'], 0.0)

    def test_invalid_embedding(self):
        payload = {
            'user': 'user3',
            'sentence': 'test',
            'category': 'test',
            'embedding': 'not_a_list'
        }
        resp = self.client.post(self.list_url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.json())
