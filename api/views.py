from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
    DestroyAPIView,
)

## Status Serializers ##
from .serializers import (
    StatusListSerializer,
)
## Product Serializers ##
from .serializers import (
	ProductListSerializer,
	ProductDetailSerializer,
)


## Order ##
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateUpdateSerializer,
)

## OrderProduct serializers ##
from .serializers import (
    OrderProductSerializer,
    OrderProductCreateUpdateSerializer,
    OrderProductQuantityUpdateSerializer
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
from .models import Profile
from .models import Order
from .models import OrderProduct
from django.contrib.auth.models import User


from .serializers import (
UserCreateSerializer,  
ProfileDetailSerializer, 
ProfileCreateUpdateSerializer
)


from rest_framework.views import APIView

from django.http import Http404
from rest_framework.response import Response
from rest_framework import status




class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class ProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'profile_id'

class ProfileUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        
        profile = self.get_object(pk)
            # request.FILES for for any type of files req 
        if(request.data.get('image')):
            data= {
                "image": request.data['image'],
                "customer": request.data['customer']
            }
        else:
            data={
                "customer":request.data['customer']
            }
        serializer = ProfileCreateUpdateSerializer(profile, data=data)
        user= User.objects.get(id=request.data['customer'])
        user.first_name= request.data['first_name']
        user.last_name= request.data['last_name']
        user.save()
        if serializer.is_valid():
            serializer.save()
            return Response(ProfileDetailSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# No need for listing 
class StatusListView(ListAPIView):
    queryset = Status.objects.filter(is_active=True)
    serializer_class = StatusListSerializer

    
class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListSerializer
	permission_classes = [AllowAny, ]
	search_fields = ['name',]
	filter_backends = [OrderingFilter, SearchFilter]


# only need list API view 
class ProductDetailView(RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'
	permission_classes = [AllowAny, ]


#  delete
# class ProductCreateView(CreateAPIView):
# 	serializer_class = ProductCreateUpdateSerializer
# 	permission_classes = [IsAdminUser,]

# 	def perform_create(self, serializer):
# 	    serializer.save(added_by=self.request.user)

      
# class ProductUpdateView(RetrieveUpdateAPIView):
# 	queryset = Product.objects.all()
# 	serializer_class = ProductCreateUpdateSerializer
# 	permission_classes = [IsAdminUser, ]
# 	lookup_field = 'id'
# 	lookup_url_kwarg = 'product_id'
####


## Order APIs views ##
class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Order.objects.filter(ordered_by=self.request.user.profile)


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'order_id'
    permission_classes = [IsAuthenticated, ]


class OrderCreateView(CreateAPIView):
    serializer_class = OrderCreateUpdateSerializer
    permission_classes =[IsAuthenticated, ]

    def perform_create(self, serializer):
      serializer.save(ordered_by=self.request.user.profile)

    # def post(self, request):
    #     pass


## Order Products APIs views

# Creating an orderProduct
class OrderProductCreateView(CreateAPIView):
    serializer_class= OrderProductCreateUpdateSerializer
    permission_classes =[IsAuthenticated, ]


# maybe we can use the same serializer as the create API view
class OrderProductQuantityUpdateView(RetrieveUpdateAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductQuantityUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'orderproduct_id'
    permission_classes = [IsAuthenticated, ] 

# No need for this view AT ALL
class OrderProductDetailView(RetrieveAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'orderproduct_id'
    permission_classes = [IsAuthenticated, ] 

class OrderProductDeleteView(DestroyAPIView):
    queryset = OrderProduct.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'orderproduct_id'
    permission_classes = [IsAuthenticated, ] 