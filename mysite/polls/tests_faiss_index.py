from django.test import TestCase
from django.urls import reverse
import json
import os
import shutil


class FAISSIndexAPITest(TestCase):
    def setUp(self):
        self.status_url = reverse('faiss-index-status')
        self.rebuild_url = reverse('faiss-index-rebuild')
        self.sync_url = reverse('faiss-index-sync')
        self.base_path = 'faiss_data/'

    def tearDown(self):
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)

    def test_index_status_initial(self):
        resp = self.client.get(self.status_url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('index_exists', data)
        self.assertIn('dimension', data)
        self.assertEqual(data['dimension'], 384)
        self.assertIn('index_type', data)
        self.assertIn('IndexFlatL2', data['index_type'])

    def test_index_rebuild(self):
        resp = self.client.post(self.rebuild_url)
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['result'], 'rebuilt')
        self.assertEqual(data['dimension'], 384)
        self.assertEqual(data['files_created'], 3)
        
        # 驗證檔案確實建立
        self.assertTrue(
            os.path.exists(os.path.join(self.base_path, 'kb_index.faiss'))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.base_path, 'kb_metadata.json'))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.base_path, 'kb_texts.pkl'))
        )

    def test_index_status_after_rebuild(self):
        # 先重建
        self.client.post(self.rebuild_url)
        
        # 再查詢狀態
        resp = self.client.get(self.status_url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['index_exists'])
        self.assertTrue(data['metadata_exists'])
        self.assertTrue(data['texts_exists'])

    def test_index_sync(self):
        resp = self.client.post(self.sync_url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['result'], 'synced')
        self.assertIn('tickets_synced', data)
        self.assertEqual(data['dimension'], 384)

    def test_dimension_384(self):
        # 驗證維度固定為 384（all-MiniLM-L6-v2）
        resp = self.client.get(self.status_url)
        data = resp.json()
        self.assertEqual(data['dimension'], 384)
        
        resp = self.client.post(self.rebuild_url)
        data = resp.json()
        self.assertEqual(data['dimension'], 384)

    def test_index_type_idmap(self):
        resp = self.client.get(self.status_url)
        data = resp.json()
        self.assertIn('IndexIDMap', data['index_type'])
        self.assertIn('IndexFlatL2', data['index_type'])
