from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

## Auth & Profile ##
from .views import (
  ProfileDetailView,
  ProfileUpdateView, 
  UserCreateAPIView
)

## Product API Views ##
from .views import (
	ProductListView,
	ProductDetailView,
)

## Status API views ##
from api.views import (
	StatusListView,
)

## Order APIs ##
from api.views import (
  OrderListView,
  OrderDetailView,
  OrderCreateView,
)

## OrderProduct APIs ##
from api.views import (
  OrderProductCreateView,
  OrderProductDeleteView,
  OrderProductQuantityUpdateView,
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

    ## Orders ##    
    path('orders/list/', OrderListView.as_view(), name='orders-list'),
    path('orders/detail/<int:order_id>/', OrderDetailView.as_view(), name='orders-detail'),
    path('orders/create/', OrderCreateView.as_view(), name='orders-create'),

    ## OrderProduct ##
    path('orderproduct/create/', 
      OrderProductCreateView.as_view(), name='orderproduct-create'),
    
    path('orderproduct/delete/<int:orderproduct_id>', 
      OrderProductDeleteView.as_view(), name='orderproduct-delete'),

    path('orderproduct/update_quantity/<int:orderproduct_id>', 
      OrderProductQuantityUpdateView.as_view(), name='orderproduct-update-quantity'),

]