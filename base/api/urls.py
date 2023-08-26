from django.urls import path
from . import views
from .views import RegisterView, LoginView, TestView, UserToGymCreateAPIView, GymView, GymListAPIView, GymRetrieveAPIView,UserGymsAPIView
from .views import GymUsersAPIView,SubscriptionCreateAPIView,UserSubscriptionsAPIView, CustomUserRetrieveAPIView

urlpatterns=[
    path('', views.get_routs),
    path('add-new-user/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('test/', TestView.as_view()),
    path('add-user-to-gym/', UserToGymCreateAPIView.as_view(), name='user-to-gym-create'),
    path('get-user-gyms/<int:user_id>/', UserGymsAPIView.as_view(), name='user-gyms'),
    path('gym-users/<int:gym_id>/', GymUsersAPIView.as_view(), name='gym-users'),
    path('add-gym/', GymView.as_view()),
    path('get-gym-by-id/<int:id>/', GymRetrieveAPIView.as_view(), name='gym-detail'),
    path('get-gyms/', GymListAPIView.as_view()),
    path('create-subscription/', SubscriptionCreateAPIView.as_view(), name='create-subscription'),
    path('user-subscriptions/<int:user_id>/', UserSubscriptionsAPIView.as_view(), name='user-subscriptions'),
    path('user/<int:id>/', CustomUserRetrieveAPIView.as_view(), name='custom-user-detail'),
]