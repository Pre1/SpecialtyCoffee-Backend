from decimal import Decimal
import requests

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
    DestroyAPIView,
)

from rest_framework.views import APIView

from django.http import Http404
from rest_framework.response import Response
from rest_framework import status



from .serializers import (

    UserCreateSerializer,
    ProfileDetailSerializer,
    ProfileCreateUpdateSerializer,

    ProductListSerializer,
    ProductDetailSerializer,

    StatusListSerializer,

    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateUpdateSerializer,

    OrderProductSerializer,
    OrderProductCreateUpdateSerializer,
    OrderProductQuantityUpdateSerializer,
)


## Permissions ##
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser
)

from rest_framework.filters import (SearchFilter, OrderingFilter)

## MODELS ##
from django.contrib.auth.models import User

from .models import (
    Product,
    Status,
    Profile,
    Order,
    OrderProduct,
)



class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class ProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'profile_id'


class ProfileDetailDetailView(RetrieveAPIView):

    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):

        profile = Profile.objects.get(customer=request.user)

        serializer = ProfileDetailSerializer(
            profile, context={"request": request})
        return Response(serializer.data)


### Old profile update API ###
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

        print("========Profile Update========")
        print(request.data)
        print("========Profile Update========")

        data = {"image": request.data['image']} if request.data.get('image') else {
            "image": None}
        serializer = ProfileCreateUpdateSerializer(profile, data=data)
        user = profile.customer
        # user.update(**request.data['customer'])

        user.first_name = request.data['customer']['first_name']
        user.last_name = request.data['customer']['last_name']
        user.save()

        if serializer.is_valid():
            serializer.save()
            return Response(ProfileDetailSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateUpdateView(APIView):

    def get_object(self, user):
        try:
            return Profile.objects.get(customer=user)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, user, format=None):
        profile = self.get_object(request.user)
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object(request.user)

        data = {"image": request.data['image']} if request.data.get('image') else {
            "image": None}

        serializer = ProfileCreateUpdateSerializer(profile, data=data)
        user = profile.customer

        user.first_name = request.data['customer']['first_name']
        user.last_name = request.data['customer']['last_name']
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
    search_fields = ['name', ]
    filter_backends = [OrderingFilter, SearchFilter]


# only need list API view
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'
    permission_classes = [AllowAny, ]


## Order APIs views ##
# this's might be not needed, check profile detail order list.
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
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(ordered_by=self.request.user.profile)


class OrderStatusUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request, order_id):

        order_obj = Order.objects.get(id=order_id)
        
        status = request.data['status']
        status_obj = Status.objects.get(id = status)

        print("request.data: ", request.data)

        serializer = OrderCreateUpdateSerializer(order_obj, data=request.data)

        #====== set up payment gatway ======#
        url = "https://api.tap.company/v2/charges"
        headers = {
            'authorization': "Bearer sk_test_XKokBfNWv6FIYuTMg5sLPjhJ",
            'content-type': "application/json"
        }
        phoneNum = '0551234567' # for testing
        total_price = order_obj.total_price
        payload = """
            {
                "amount": "%s",
                "currency": "SAR",
                "threeDSecure": "true",
                "customer": {
                    "first_name": "%s",
                    "last_name": "%s",
                    "email": "%s",
                    "phone": {
                        "country_code": "966",
                        "number": "%s"
                    }
                },
                "source": {
                    "id": "src_all"
                },
                "redirect": {
                    "url": "http://localhost:3000/profile"
                }
            }
        """ %(
                total_price,
                order_obj.ordered_by.customer.first_name,
                order_obj.ordered_by.customer.last_name,
                order_obj.ordered_by.customer.email,
                phoneNum
            )

        print("paylod", payload)

        response = requests.post(url, data=payload, headers=headers)

        payment_url = response.json()['transaction']['url']
        print(payment_url)
        if serializer.is_valid():
            serializer.save()
            return Response({"order_status": serializer.data, "payment_url": payment_url})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order Products APIs views

# Creating an orderProduct


class OrderProductCreateView(CreateAPIView):
    serializer_class = OrderProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):

        order_id = request.data['order']
        product_id = request.data['product']
        quantity = request.data['quantity']

        order_obj = Order.objects.get(id=order_id)
        product_obj = Product.objects.get(id=product_id)

        new_order_prod, created = order_obj.order_products.get_or_create(
            product=product_obj)

        if created:
            new_order_prod.total_price = product_obj.price * Decimal(quantity)
            new_order_prod.quantity = quantity
        else:
            new_order_prod.quantity += int(quantity)
            new_order_prod.total_price += product_obj.price * Decimal(quantity)

        new_data = {
            'order': order_id,
            'product': product_id,
            'quantity': new_order_prod.quantity
        }

        # new_order_prod.save()

        serializer = self.serializer_class(new_order_prod, data=new_data)

        print("=========Serializer========")
        print("serializer: ", serializer)
        print("vars(serializer): ", vars(serializer))
        print("=========END Serializer END========")

        if serializer.is_valid():
            serializer.save()
            return Response(OrderProductSerializer(new_order_prod).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# maybe we can use the same serializer as the create API view


class OrderProductQuantityUpdateView(RetrieveUpdateAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductQuantityUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'orderproduct_id'
    permission_classes = [IsAuthenticated, ]

    def perform_update(self, serializer):
        print("=========OrderProductQuantityUpdateView========")
        print("serializer: ", serializer)
        print("vars(serializer): ", vars(serializer))

        print("serializer.instance: ", serializer.instance)
        quantity = serializer.validated_data['quantity']
        order_prod = serializer.instance
        prod_obj = order_prod.product

        order_prod.total_price = prod_obj.price * Decimal(quantity)

        serializer.save()

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
