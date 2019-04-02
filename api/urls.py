from django.urls import path
from .views import UserCreateAPIView
from rest_framework_jwt.views import obtain_jwt_token
from api.views import (
		StatusListView,
		StatusCreateView,
		StatusUpdateView,
)

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('api/status/create/', StatusCreateView.as_view(), name='api-status-create'),
    path('api/list/', StatusListView.as_view(), name='api-status-list'),
    path('api/status/update', StatusUpdateView.as_view(), name='api-status-update')


]