from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import (
  ProfileDetailView,
  ProfileUpdateView, 
  UserCreateAPIView
)

## API Views ##
from .views import (
	UserCreateAPIView,
	ProductListView,
	ProductDetailView,
)

from api.views import (
	StatusListView,
)

urlpatterns = [
  ## Auth ##
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('profile/update/<int:pk>/',ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/detail/<int:profile_id>/', ProfileDetailView.as_view(), name='profile-detail'),

    ## Status ##
    path('status/list/', StatusListView.as_view(), name='status-list'),
  
    ## Products ##
    path('products/list/', ProductListView.as_view(), name='products-list'),

    path('products/detail/<int:product_id>/',
         ProductDetailView.as_view(), name='products-detail'),
]