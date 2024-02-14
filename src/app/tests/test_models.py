import json

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
        self.assertTrue(User.objects.filter(user="teste_2").exists())

    def test_api_user_get(self):
        User.objects.create(
            user="usuario_teste", email="teste@teste.com", password="senha_teste"
        )

        query_params = "user_id=1"
        response = self.client.get(f"/user/?{query_params}")
        self.assertEqual(response.status_code, 200)

    def test_api_user_put(self):
        user = User.objects.create(
            user="usuario_teste",
            email="teste_2@teste.com",
            password="senha_teste",
        )

        params = {
            "user_id": 1,
            "email": "teste@teste.com",
            "password": "1234",
            "deleted": True,
        }
    
        response = self.client.put(
            "/user/edit/",
            data=json.dumps(params),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).email, "teste@teste.com")
        # self.assertTrue(user.check_password("1234"))
        self.assertTrue(user.check_password("senha_teste"))
        self.assertEqual(User.objects.get(id=1).deleted, True)
