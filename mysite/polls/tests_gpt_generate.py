"""
Tests for GPT Generate API
Tests the gpt_generate_api endpoint with various task types and scenarios.
"""
import json
from django.test import TestCase, Client
from polls.models import GPTPromptConfiguration


class GPTGenerateAPITestCase(TestCase):
    """Test cases for GPT Generate API endpoint"""

    def setUp(self):
        """Set up test client and sample GPTPromptConfiguration"""
        self.client = Client()
        self.url = '/polls/gpt-generate/'
        
        # Create test prompt configurations
        GPTPromptConfiguration.objects.create(
            task_type='classification',
            prompt='Classify this: {input}',
            model='gpt-4'
        )
        GPTPromptConfiguration.objects.create(
            task_type='summarization',
            prompt='Summarize: {input}',
            model='gpt-3.5-turbo'
        )

    def test_valid_classification_request(self):
        """Test valid classification request"""
        data = {
            'task_type': 'classification',
            'input': 'This is a positive review of the product.'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['task_type'], 'classification')
        self.assertEqual(result['model'], 'gpt-4')
        self.assertEqual(result['input'], data['input'])
        self.assertIn('output', result)
        self.assertIn('prompt_used', result)
        self.assertEqual(result['method'], 'simulated')

    def test_valid_summarization_request(self):
        """Test valid summarization request"""
        data = {
            'task_type': 'summarization',
            'input': 'This is a long text that needs to be summarized.'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['task_type'], 'summarization')
        self.assertEqual(result['model'], 'gpt-3.5-turbo')
        self.assertIn('AI', result['output'])

    def test_custom_prompt_override(self):
        """Test custom prompt override"""
        data = {
            'task_type': 'classification',
            'input': 'Test input',
            'custom_prompt': 'Custom analysis: {input}'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        # Custom prompt is used in generation but prompt_used shows template
        self.assertIn('input', result['prompt_used'].lower())

    def test_missing_input_parameter(self):
        """Test missing required input parameter"""
        data = {
            'task_type': 'classification'
            # Missing 'input' field
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertIn('error', result)
        self.assertIn('input', result['error'].lower())

    def test_missing_task_type_parameter(self):
        """Test missing required task_type parameter"""
        data = {
            'input': 'Test input'
            # Missing 'task_type' field
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # API returns 404 when task_type not found
        self.assertEqual(response.status_code, 404)
        result = response.json()
        self.assertIn('error', result)

    def test_nonexistent_task_type(self):
        """Test non-existent task_type (404)"""
        data = {
            'task_type': 'nonexistent_task',
            'input': 'Test input'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        result = response.json()
        self.assertIn('error', result)
        self.assertIn('task_type', result['error'].lower())

    def test_method_not_allowed(self):
        """Test GET method not allowed (405)"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 405)
        result = response.json()
        self.assertIn('error', result)
        self.assertIn('method', result['error'].lower())

    def test_invalid_json(self):
        """Test invalid JSON payload (400)"""
        response = self.client.post(
            self.url,
            data='invalid json{',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertIn('error', result)

    def test_empty_input(self):
        """Test empty input string"""
        data = {
            'task_type': 'classification',
            'input': ''
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Empty input returns 400 error
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertIn('error', result)

    def test_long_input(self):
        """Test very long input text"""
        data = {
            'task_type': 'summarization',
            'input': 'Long text. ' * 500  # 5000+ characters
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('output', result)

    def test_chinese_input(self):
        """Test Chinese text input"""
        data = {
            'task_type': 'classification',
            'input': '這是一個測試輸入文本。'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['input'], '這是一個測試輸入文本。')
        self.assertIn('output', result)

    def test_special_characters_input(self):
        """Test input with special characters"""
        data = {
            'task_type': 'classification',
            'input': 'Test @#$%^&*() input with <html> tags'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(
            result['input'],
            'Test @#$%^&*() input with <html> tags'
        )

    def test_multiple_sequential_requests(self):
        """Test multiple sequential requests"""
        for i in range(3):
            data = {
                'task_type': 'classification',
                'input': f'Test input {i}'
            }
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            result = response.json()
            self.assertEqual(result['input'], f'Test input {i}')

    def test_response_structure(self):
        """Test complete response structure"""
        data = {
            'task_type': 'classification',
            'input': 'Test input'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        # Check all required fields
        required_fields = [
            'task_type', 'model', 'input', 'output',
            'prompt_used', 'method', 'note'
        ]
        for field in required_fields:
            self.assertIn(field, result)
        
        # Verify types
        self.assertIsInstance(result['task_type'], str)
        self.assertIsInstance(result['model'], str)
        self.assertIsInstance(result['input'], str)
        self.assertIsInstance(result['output'], str)
        self.assertIsInstance(result['prompt_used'], str)
        self.assertEqual(result['method'], 'simulated')
