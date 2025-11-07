from django.test import TestCase
from django.urls import reverse
from polls.models import UploadedFile
import json


class UploadedFileAPITest(TestCase):
    def setUp(self):
        self.list_url = reverse('uploaded-file-list')

    def test_create_valid_xlsx_file(self):
        data = {
            'filename': 'test.xlsx',
            'stored_filename': 'result_20250101_120000.xlsx',
            'file_size': 1024,
            'file_path': 'uploads/'
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(
            UploadedFile.objects.filter(filename='test.xlsx').exists()
        )

    def test_create_invalid_format(self):
        data = {
            'filename': 'test.csv',
            'stored_filename': 'result_20250101_120001.csv',
            'file_size': 1024,
            'file_path': 'uploads/'
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        error_msg = resp.json().get('error', '')
        self.assertIn('.xlsx', error_msg)

    def test_create_oversized_file(self):
        MAX_SIZE = 10 * 1024 * 1024 + 1  # 10MiB + 1 byte
        data = {
            'filename': 'huge.xlsx',
            'stored_filename': 'result_20250101_120002.xlsx',
            'file_size': MAX_SIZE,
            'file_path': 'uploads/'
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        error_msg = resp.json().get('error', '')
        self.assertIn('10MiB', error_msg)

    def test_create_max_size_file(self):
        MAX_SIZE = 10 * 1024 * 1024  # exactly 10MiB
        data = {
            'filename': 'max.xlsx',
            'stored_filename': 'result_20250101_120003.xlsx',
            'file_size': MAX_SIZE,
            'file_path': 'uploads/'
        }
        resp = self.client.post(
            self.list_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 201)

    def test_delete_file(self):
        file_obj = UploadedFile.objects.create(
            filename='delete.xlsx',
            stored_filename='result_20250101_120004.xlsx',
            file_size=2048,
            file_path='uploads/'
        )
        url = reverse('uploaded-file-detail', args=[file_obj.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            UploadedFile.objects.filter(id=file_obj.id).exists()
        )

    def test_list_files(self):
        UploadedFile.objects.create(
            filename='list1.xlsx',
            stored_filename='result_20250101_120005.xlsx',
            file_size=512,
            file_path='uploads/'
        )
        UploadedFile.objects.create(
            filename='list2.xlsx',
            stored_filename='result_20250101_120006.xlsx',
            file_size=1024,
            file_path='uploads/'
        )
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        files = resp.json().get('files', [])
        self.assertGreaterEqual(len(files), 2)

    def test_get_file_detail(self):
        file_obj = UploadedFile.objects.create(
            filename='detail.xlsx',
            stored_filename='result_20250101_120007.xlsx',
            file_size=4096,
            file_path='uploads/'
        )
        url = reverse('uploaded-file-detail', args=[file_obj.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['filename'], 'detail.xlsx')
        self.assertEqual(data['file_size'], 4096)
