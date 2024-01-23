import logging

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError

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
				user.password = data['password']

				user.save()

				return Response({"msg": "Usuário criado com sucesso"}, status=status.HTTP_200_OK)
			
			else:
				return Response({"msg": "Email ou usuário já existem"}, status=status.HTTP_400_BAD_REQUEST)
		
		except IntegrityError as error:
			msg = "Email já cadastrado"
			logging.error(msg)
			logging.error({error})

			return Response([{'msg': msg}], status=status.HTTP_403_FORBIDDEN)

	def get(self,request):
		"""
			Retorna o usuário especifico para login
			
			query params:
				user: string obrigatorio
				password: string obrigatorio

		"""
		user = request.GET.get('user')
		password = request.GET.get('password')
		
		authorized_user = User.objects.filter(user=user, password=password)
		
		if authorized_user:
			return Response({'msg': "Login feito com sucesso"}, status=status.HTTP_200_OK)
		
		else:
			return Response({'msg': 'Usuário ou senha incorretos'}, status=status.HTTP_401_UNAUTHORIZED)

	def put (self, request):
		"""
			Altera os dados do usuário: senha e email

			payload:
				{
					user_id : int obrigatorio
					email: string opcional
					password: string opcional
				}

		"""	

		try:

			data = request.data
		
			change_user = User.objects.get(id=data['user_id'])
			
			if data['email']:
				change_user.email = data['email']

			if data['password']:
				change_user.password = data['password']
			
			change_user.save()

			return Response({"msg": "Usuário alterado com sucesso"}, status=status.HTTP_200_OK)
			
		except Exception as error:
			logging.exception(str(error))
			return Response([{'msg': 'Erro ao salvar alterações'}], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TasksViews(APIView):
	def post(self, request):
		pass