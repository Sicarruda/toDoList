import json

from django.test import TestCase
from app.models import *
from django.contrib.auth.hashers import check_password


class UserTestCase(TestCase):

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
        user = {
            "user": "usuario_teste",
            "email": "teste@teste.com",
            "password": "senha_teste",
        }


        User.objects.create(
            user="usuario_teste", email="teste@teste.com", password="senha_teste"
        )

        User.objects.create(
            user="usuario_teste_2", email="teste_2@teste.com", password="senha_teste_2"
        )

        query_params = "user_id=1"
        response = self.client.get(f"/user/?{query_params}")

        response_data = json.loads(response.content)
        user_return = response_data["user"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user_return), 1)
        self.assertIn(user["email"], [item["email"] for item in user_return])

    def test_api_user_put(self):
        User.objects.create(
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
            "/user/edit/", data=json.dumps(params), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).email, "teste@teste.com")
        self.assertFalse(check_password("senha_teste", User.objects.get(id=1).password))
        self.assertTrue(check_password("1234", User.objects.get(id=1).password))
        self.assertEqual(User.objects.get(id=1).deleted, True)


class TasksTestCase(TestCase):
    def test_api_task_post(self):
        user = User.objects.create(
            user="usuario_teste",
            email="teste@teste.com",
            password="senha_teste",
        )

        params = {"task": "La la lá", "user_id": 1}

        response = self.client.post("/task/add-task/", params)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ListToDo.objects.filter(id=1).exists())
        self.assertTrue(ListToDo.objects.filter(task="La la lá").exists())

    def test_api_task_get(self):
        User.objects.create(
            user="usuario_teste",
            email="teste@teste.com",
            password="senha_teste",
        )

        task1_ok = {"task": "La la lá", "user_id": User.objects.get(id=1)}
        task2_ok = {"task": "Lu lu lu", "user_id": User.objects.get(id=1)}
        task_deleted = {
            "task": "Li li li",
            "deleted": True,
            "user_id": User.objects.get(id=1),
        }

        ListToDo.objects.create(user_id=1, task="La la lá")
        ListToDo.objects.create(user_id=1, task="Lu lu lu")
        ListToDo.objects.create(user_id=1, task="Li li li", deleted=True)

        query_params = "user_id=1"

        response = self.client.get(f"/task/?{query_params}")

        # Converte a resposta JSON para um dicionário
        response_data = json.loads(response.content)
        tasks_list = response_data["tasks"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ListToDo.objects.get(id=1).task, task1_ok["task"])
        self.assertEqual(ListToDo.objects.get(id=2).task, task2_ok["task"])
        self.assertIn(task1_ok["task"], [item["task"] for item in tasks_list])
        self.assertIn(task2_ok["task"], [item["task"] for item in tasks_list])
        self.assertNotIn(task_deleted["task"], [item["task"] for item in tasks_list])

    def test_api_task_put(self):
        User.objects.create(
            user="usuario_teste",
            email="teste_2@teste.com",
            password="senha_teste",
        )

        ListToDo.objects.create(user_id=1, task="La la lá")

        task = {
            "task_id ": 1,
            "task": "li li li",
            "is_complete": True,
            "deleted": True,
        }

        response = self.client.put(
            "/task/edit/", data=json.dumps(task), content_type="application/json"
        )

        print(response)

        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(ListToDo.objects.get(id=1).task, "li li li")
        # self.assertEqual(ListToDo.objects.get(id=1).deleted, True)
        # self.assertEqual(ListToDo.objects.get(id=1).is_complete, True)
