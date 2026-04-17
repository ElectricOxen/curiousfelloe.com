from django.test import TestCase, Client
from django.urls import reverse


class LandingPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_returns_200(self):
        response = self.client.get(reverse('landing:home'))
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
