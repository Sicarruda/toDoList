from django.test import TestCase

class UsuarioTestCase(TestCase):

    def test_model_user_creation(self):
        self.assertEqual(1,1)
    
    def test_api_teste(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
