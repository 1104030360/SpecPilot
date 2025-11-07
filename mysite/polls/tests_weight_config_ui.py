from django.test import TestCase, Client
from django.urls import reverse

class WeightConfigUITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('spec_generator')

    def test_weight_config_form_render(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'form id="weight-config-form"')
        self.assertContains(response, 'input type="number" id="score-a"')
        self.assertContains(response, 'input type="number" id="score-b"')
        self.assertContains(response, 'input type="number" id="score-c"')
        self.assertContains(response, 'input type="number" id="score-d"')
        self.assertContains(response, 'button type="submit"')
        self.assertContains(response, 'id="weight-error"')
        self.assertContains(response, 'id="weight-config-list"')

    def test_weight_config_list_render(self):
        response = self.client.get(self.url)
        self.assertContains(response, '現有權重配置')
        self.assertContains(response, '<ul>')
