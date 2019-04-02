from django.urls import path
from .views import (ProfileDetailView, ProfileUpdateView, UserCreateAPIView)
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('profile/update/<int:pk>/',ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/detail/<int:profile_id>/', ProfileDetailView.as_view(), name='profile-detail'),

]