from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

## Auth & Profile ##
from .views import (

    UserCreateAPIView,
    ProfileDetailView,
    ProfileDetailDetailView,
    ProfileUpdateView,
    ProfileUpdateUpdateView,

    ProductListView,
    ProductDetailView,

    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderStatusUpdateView,

    StatusListView,

    OrderProductCreateView,
    OrderProductDeleteView,
    OrderProductQuantityUpdateView,
    OrderProductDetailView,
)


urlpatterns = [
    ## Auth ##
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),

    path('profile/update/<int:pk>/',
         ProfileUpdateView.as_view(), name='profile-update'),

    path('profile/update/',
         ProfileUpdateUpdateView.as_view(), name='profile-update-update'),

    path('profile/detail/<int:profile_id>/',
         ProfileDetailView.as_view(), name='profile-detail'),

    path('profile/detail/',
         ProfileDetailDetailView.as_view(), name='profile-detail-detail'),

    ## Status ##
    path('status/list/', StatusListView.as_view(), name='status-list'),

    ## Products ##
    path('products/list/', ProductListView.as_view(), name='products-list'),

    path('products/detail/<int:product_id>/',
         ProductDetailView.as_view(), name='products-detail'),

    ## Orders ##
    path('orders/list/', OrderListView.as_view(), name='orders-list'),
    path('orders/detail/<int:order_id>/',
         OrderDetailView.as_view(), name='orders-detail'),
    path('orders/create/', OrderCreateView.as_view(), name='orders-create'),

    path('orders/update/<int:order_id>',
         OrderStatusUpdateView.as_view(), name='orders-status-update'),

    ## OrderProduct ##
    path('orderproduct/create/',
         OrderProductCreateView.as_view(), name='orderproduct-create'),

    path('orderproduct/delete/<int:orderproduct_id>/',
         OrderProductDeleteView.as_view(), name='orderproduct-delete'),

    path('orderproduct/update_quantity/<int:orderproduct_id>/',
         OrderProductQuantityUpdateView.as_view(), name='orderproduct-update-quantity'),

    path('orderproduct/detail/<int:orderproduct_id>/',
         OrderProductDetailView.as_view(), name='orderproduct-detail'),

]
