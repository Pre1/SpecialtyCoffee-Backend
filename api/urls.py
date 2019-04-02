from django.urls import path

## API Views ##
from .views import (
	UserCreateAPIView,
	ProductListView,
	ProductDetailView,
	ProductCreateView,
	ProductUpdateView
)

from rest_framework_jwt.views import obtain_jwt_token
from api.views import (
		StatusListView,
		StatusCreateView,
		StatusUpdateView,
)

urlpatterns = [
  ## Auth ##
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),


    ## Status ##
    path('status/create/', StatusCreateView.as_view(), name='status-create'),
    path('status/list/', StatusListView.as_view(), name='status-list'),
    path('status/update', StatusUpdateView.as_view(), name='status-update')
  
    ## Products ##
    path('products/list/', ProductListView.as_view(), name='products-list'),

    path('products/detail/<int:product_id>/',
         ProductDetailView.as_view(), name='products-detail'),

    path('products/create/',
         ProductCreateView.as_view(), name='products-create'),
    
    path('products/update/<int:product_id>/',
         ProductUpdateView.as_view(), name='products-update'),

]

