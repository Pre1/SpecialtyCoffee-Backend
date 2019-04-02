
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
)

## Status Serializers ##
from .serializers import (
    StatusListSerializer,
    StatusCreateUpdateSerializer
)
## Product Serializers ##
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
from .models import Status

class StatusListView(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusListSerializer
    search_fields = ['title', 'is_active']

    
class StatusCreateView(CreateAPIView):
    serializer_class = StatusCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        
class StatusUpdateView(RetrieveUpdateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusCreateUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'status_id'
    
    
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

