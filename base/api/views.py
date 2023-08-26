from django.http import JsonResponse
from django.utils.encoding import smart_str
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, UserToGymSerializer, GymSerializer, SubscriptionSerializer
from base.models import CustomUser, Gym, UserToGym, Subscription
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import generics
import jwt, datetime
from backend.settings import SECRET_KEY
from .permissions import IsRoleAdmin, IsRoleUser, IsRoleMember
from datetime import date


# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email = email).first()
        if user is None:
            raise AuthenticationFailed('User not found for given email address!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'role': user.role_id,
            'username': user.email
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return JsonResponse({
            'jwt': token,
            'role': user.role_id,
            'id': user.id,
        })

def get_routs(request):
    routes = ['/api/token', '/api/token/refresh']
    return JsonResponse(routes, safe=False)

class TestView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsRoleAdmin, IsRoleUser]
    def get(self, request):
        return JsonResponse({
            'test': 'test'
        })

class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'

class UserToGymCreateAPIView(generics.CreateAPIView):
    queryset = UserToGym.objects.all()
    serializer_class = UserToGymSerializer

class UserGymsAPIView(generics.ListAPIView):
    serializer_class = GymSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']  # Extract user_id from URL
        gym_ids = UserToGym.objects.filter(user_id=user_id).values_list('gym_id', flat=True)
        return Gym.objects.filter(id__in=gym_ids)
    

class GymUsersAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        gym_id = self.kwargs['gym_id']  # Extract gym_id from URL
        user_ids = UserToGym.objects.filter(gym_id=gym_id).values_list('user_id', flat=True)
        user_id_list = list(user_ids)
        
        users = CustomUser.objects.filter(id__in=user_id_list)
        return users

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

class GymView(APIView):
    def post(self, request):
        serializer = GymSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)
    
    def get(self, request):
        queryset = Gym.objects.all()
        return JsonResponse(queryset, safe=False)

class GymListAPIView(generics.ListAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        gym_list = list(serializer.data)
        gym_dict = {gym_data['id']: gym_data for gym_data in gym_list}
        return JsonResponse(gym_dict)

class GymRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = GymSerializer
    lookup_field = 'id'

    def get_queryset(self):
        gym_id = self.kwargs['id']
        return Gym.objects.filter(id=gym_id)
    
class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class UserSubscriptionsAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']  # Extract user_id from URL
        current_date = date.today()
        subscriptions = Subscription.objects.filter(user_id=user_id, date_to__gt=current_date)
        return subscriptions

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(status=404)

def get_gym_by_id(request):
    pass