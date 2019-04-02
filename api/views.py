## API Views ##
from rest_framework.generics import (
	
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
)

## Serializers ##
from .serializers import (
	UserCreateSerializer,
	ProductListSerializer,
	ProductDetailSerializer,
	ProductCreateUpdateSerializer,
)

## Permissions ##
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser
)

from rest_framework.filters import (SearchFilter, OrderingFilter)


## MODELS ##
from .models import Product

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer


class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListSerializer
	permission_classes = [AllowAny, ]
	search_fields = ['name',]
	filter_backends = [OrderingFilter, SearchFilter]


class ProductDetailView(RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'
	permission_classes = [AllowAny, ]




class ProductCreateView(CreateAPIView):
	serializer_class = ProductCreateUpdateSerializer
	permission_classes = [IsAdminUser,]


	def perform_create(self, serializer):
	    serializer.save(added_by=self.request.user)


class ProductUpdateView(RetrieveUpdateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductCreateUpdateSerializer
	permission_classes = [IsAdminUser, ]
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'


