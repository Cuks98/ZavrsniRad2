from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import CustomUserSerializer
from django.http import JsonResponse
# Create your views here.

class RegisterView(APIView):
    def register(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)