from django.shortcuts import render
from rest_framework.views import APIView


class UserView(APIView):
	def post(self, request):
		try:
			data = request.data
			
		except:
			pass