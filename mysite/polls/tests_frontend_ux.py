from django.test import TestCase, Client
from django.urls import reverse

class FrontendUXTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('spec_generator')

    def test_form_required_fields(self):
        data = {
            'project_goal': '',
            'core_features': '',
            'technical_constraints': '',
            'target_audience': '',
        }
        response = self.client.post(self.url, data)
        self.assertContains(response, '請填寫所有欄位')
        self.assertContains(response, 'form-error')

    def test_button_state(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'button type="submit"')

    def test_error_message_display(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'form-error')

    def test_section_expand_collapse(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<details')
        self.assertContains(response, '<summary>背景</summary>')
        self.assertContains(response, '<summary>目標</summary>')

    def test_copy_download_buttons(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'onclick="copySection')
        self.assertContains(response, 'onclick="downloadSection')

    def test_result_preview_block(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'id="result-container"')
        self.assertContains(response, 'class="result-title"')
        self.assertContains(response, 'id="result"')
