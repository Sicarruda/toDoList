import logging

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from app.models import User, ListToDo


class UserView(APIView):
	def post(self, request):
		"""
			Cria cadastro de usuário e senha no banco
				payload:
					{
						user: string obrigatorio
						email: string opcional
						password: string obrigatorio
					}
		"""
		data = request.data
		user = User()
		
		try:

			new_user = User.objects.filter(user=data['user'], email=data['email'])

			if not new_user:
				user.user = data['user']
				user.email = data['email']
				user.set_password(data['password'])

				user.save()

				return Response({"msg": "Usuário criado com sucesso"}, status=status.HTTP_201_CREATED)
			
			else:
				return Response({"msg": "Email ou usuário já existem"}, status=status.HTTP_400_BAD_REQUEST)
		
		except IntegrityError as error:
			logging.exception(str(error))
			return Response([{'msg': 'Email já cadastrado'}], status=status.HTTP_403_FORBIDDEN)

	def get(self,request):
		"""
			Retorna o usuário especifico 
			query params:
				user_id: string obrigatorio
		"""
		user_id = request.GET.get('user_id')
		
		user = User.objects.filter(id=user_id).values()
		
		if user:
			return Response({'msg': "Usuário retornado com sucesso", "user": user}, status=status.HTTP_200_OK)
		
		else:
			return Response({'msg': 'Falha ao retornar usuário'}, status=status.HTTP_400_BAD_REQUEST)

	def put (self, request):
		"""
			Altera os dados do usuário: senha e email

			payload:
				{
					user_id : int obrigatorio
					email: string opcional
					password: string opcional
					deleted: booliano opcional
				}
		"""	

		try:

			data = request.data
		
			change_user = User.objects.get(id=data['user_id'])
			
			if data['email']:
				change_user.email = data['email']

			if data['password']:
				change_user.set_password(data['password'])
			
			if data['deleted']:
				change_user.deleted = data['deleted']
			
			change_user.save()

			return Response({"msg": "Usuário alterado com sucesso"}, status=status.HTTP_200_OK)
			
		except Exception as error:
			logging.exception(str(error))
			return Response([{'msg': 'Erro ao salvar alterações'}], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskViews(APIView):
	def post(self, request):
		"""
			Cria nova tarefa 
			payload:
					{
						task: string obrigatorio
						user_id: int obrigatorio
					}
		"""
		data = request.data
		task = ListToDo()

		try:
			user = User.objects.get(id=data["user_id"])

			if not user:
				return Response([{'msg': "Usuário não encontrado"}], status=status.HTTP_403_FORBIDDEN)

			task.task = data['task']
			task.user = user

			task.save()
			return Response({"msg": "Task criada com sucesso"}, status=status.HTTP_201_CREATED)

		except Exception as error:
			logging.exception(str(error))
			return Response([{'msg': 'Erro ao salvar alterações'}], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def get(self, request):
		"""
			Retorna as tasks não deletadas do usuário 
			query params:
				user_id: string obrigatorio
		"""
		
		try:
			user_id = request.GET.get('user_id')

			user = User.objects.get(id=user_id)

			if not user_id and user_id:
				return Response({"msg": "Usuario não encontrado"}, status=status.HTTP_400_BAD_REQUEST)

			user_tasks = ListToDo.objects.filter(user = user, deleted=False).values()

			return Response({'msg':'Lista de tarefas obtida com sucesso', 'tasks': user_tasks}, status=status.HTTP_200_OK)
		
		except Exception as error:
			logging.exception(str(error))
			return Response([{'msg': 'Erro ao buscar tarefas'}], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def put(self, request):
		"""
			Edita as taks do usuário
				payload:
				{
					task_id : int obrigatorio
					task: string opcional
					is_complete: booliano opcional
					deleted: booliano opcional
				}
		"""

		try:
			data = request.data
			
			task = ListToDo.objects.get(id=data["task_id"])

			if data["is_complete"]:
				task.is_complete = data["is_complete"]
			
			if data["task"]:
				task.task = data["task"]

			if data["deleted"]:
				task.deleted = data["deleted"]

			task.save()

			return Response([{"msg": "Tarefa alterada com sucesso"}], status=status.HTTP_200_OK )
	
		except Exception as error:
			logging.exception(str(error))
			return Response([{'msg': 'Erro ao salvar alterações'}], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class loginView(APIView):
	def post(self, request):
		"""
			Login do usuário:
				payload:{
					user: string obrigatoria
					password: string obrigatoria
				}
		"""
		try:
			
			data = request.data

			authorized_user = User.objects.get(user=data["user"]) 

			if check_password(data["password"], authorized_user.password):
				return Response([{"msg": "Usuário autenticado"}], status=status.HTTP_200_OK)
			else:
				return Response([{'msg': 'Usuario ou senha incorretos'}], status=status.HTTP_401_UNAUTHORIZED)

		except Exception as error:
			logging.exception(str(error))
			return Response([{'msg': 'Falha na chamada'}], status=status.HTTP_400_BAD_REQUEST)