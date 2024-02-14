from django.test import TestCase
from app.models import *


class UsuarioTestCase(TestCase):

    def test_api_user_post(self):
        params = {
            "user": "teste_2",
            "email": "teste_2@teste.com",
            "password": "1234",
        }
        
        response = self.client.post("/user/add-user/", params)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(user='teste_2').exists())

    def test_api_user_get(self):
        User.objects.create(
            user="usuario_teste",
            email="teste@teste.com",
            password="senha_teste"
            )
        query_params = "user_id=1"
        response = self.client.get(f"/user/?{query_params}")
        self.assertEqual(response.status_code, 200)
