from django.test import TestCase, Client
from django.urls import reverse
from polls.models import GPTPromptConfiguration
import json

class GPTPromptConfigurationAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('gpt_prompt_list')
        self.item = GPTPromptConfiguration.objects.create(
            task_type='classification', prompt='請分類', model='gpt-3.5-turbo'
        )

    def test_create_prompt(self):
        payload = {
            'task_type': 'generation',
            'prompt': '請生成一段文字',
            'model': 'gpt-4'
        }
        resp = self.client.post(self.list_url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('id', resp.json())

    def test_get_prompt_list(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('prompts', resp.json())
        self.assertGreaterEqual(len(resp.json()['prompts']), 1)

    def test_update_prompt(self):
        url = reverse('gpt_prompt_detail', args=[self.item.id])
        payload = {'prompt': '請分類這些句子'}
        resp = self.client.put(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.prompt, '請分類這些句子')

    def test_delete_prompt(self):
        url = reverse('gpt_prompt_detail', args=[self.item.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(GPTPromptConfiguration.objects.filter(id=self.item.id).exists())

    def test_invalid_prompt(self):
        payload = {
            'task_type': 'summarization',
            'prompt': '',
            'model': 'gpt-3.5-turbo'
        }
        resp = self.client.post(self.list_url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.json())
