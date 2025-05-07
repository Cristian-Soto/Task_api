from django.test import TestCase
from django.urls import reverse

class HelloWorldTestCase(TestCase):
    def test_hello_world_endpoint(self):
        response = self.client.get(reverse('hello_world'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hola, mundo"})
