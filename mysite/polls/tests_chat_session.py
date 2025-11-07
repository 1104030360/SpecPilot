from django.test import TestCase
from django.urls import reverse
from polls.models import ChatSession
import json


class ChatSessionAPITest(TestCase):
    def setUp(self):
        self.list_url = reverse('chat-session-list')
        self.valid_messages = [
            {'role': 'user', 'content': '你好'},
            {'role': 'assistant', 'content': '您好，有什麼可以幫您？'}
        ]

    def test_create_valid_session(self):
        data = {
            'session_id': 'chat_20250101_120000',
            'title': '測試會話',
            'messages': self.valid_messages
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(
            ChatSession.objects.filter(
                session_id='chat_20250101_120000'
            ).exists()
        )

    def test_create_invalid_role(self):
        data = {
            'session_id': 'chat_20250101_120001',
            'title': '測試會話',
            'messages': [{'role': 'unknown', 'content': 'test'}]
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        error_msg = resp.json().get('error', '')
        self.assertIn('role', error_msg.lower())

    def test_create_missing_content(self):
        data = {
            'session_id': 'chat_20250101_120002',
            'title': '測試會話',
            'messages': [{'role': 'user'}]
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        error_msg = resp.json().get('error', '')
        self.assertIn('content', error_msg.lower())

    def test_update_session(self):
        session = ChatSession.objects.create(
            session_id='chat_20250101_120003',
            title='舊標題',
            messages=self.valid_messages
        )
        url = reverse('chat-session-detail', args=[session.session_id])
        new_messages = self.valid_messages + [
            {'role': 'user', 'content': '再見'}
        ]
        data = {'title': '新標題', 'messages': new_messages}
        resp = self.client.put(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        session.refresh_from_db()
        self.assertEqual(session.title, '新標題')
        self.assertEqual(len(session.messages), 3)

    def test_delete_session(self):
        session = ChatSession.objects.create(
            session_id='chat_20250101_120004',
            title='待刪除',
            messages=self.valid_messages
        )
        url = reverse('chat-session-detail', args=[session.session_id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            ChatSession.objects.filter(
                session_id='chat_20250101_120004'
            ).exists()
        )

    def test_multi_turn_messages(self):
        messages = [
            {'role': 'user', 'content': '第一輪'},
            {'role': 'assistant', 'content': '回覆一'},
            {'role': 'user', 'content': '第二輪'},
            {'role': 'assistant', 'content': '回覆二'},
            {'role': 'user', 'content': '第三輪'},
        ]
        data = {
            'session_id': 'chat_20250101_120005',
            'title': '多輪對話',
            'messages': messages
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 201)
        session = ChatSession.objects.get(
            session_id='chat_20250101_120005'
        )
        self.assertEqual(len(session.messages), 5)
