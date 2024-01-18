from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from models import User, ListToDo


class UserView(APIView):
	def post(self, request):
		try:
			data = request.data
			user = User()

			new_user = User.objects.filter(user=data.user, email=data.email)

			if not new_user:
				user.user = data.user
				user.email = data.email
				user.password = data.password

				user.save()

				return Response({"msg": "Usuário criado com sucesso"}, status=status.HTTP_200_OK)
			else:
				return Response({"msg": ""})
		except:
			pass