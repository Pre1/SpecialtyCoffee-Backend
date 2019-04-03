from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings


## MODELS ##
from .models import (
  Profile,
  Product,
  Status,
  OrderProduct,
  Order,
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password',
            'first_name', 'last_name', 'email', 'token', ]

    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email)
        new_user.set_password(password)
        new_user.save()

        # Saving the user to a new profile:
        new_profile = Profile(customer=new_user)
        new_profile.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(new_user)
        token = jwt_encode_handler(payload)
        validated_data['token'] = token
        return validated_data


class ProfileDetailSerializer(serializers.ModelSerializer):
    customer = UserSerializer()

    class Meta:
        model = Profile
        fields = ['customer', 'image']


class ProfileCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['customer', 'image']


class StatusListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ['title', 'is_active']


class ProductListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
		view_name="products-detail",
		lookup_field="id",
		lookup_url_kwarg="product_id"
	)

	class Meta:
		model = Product
		fields = ['id', 'detail', 'name',
				  'image', 'price', 'is_avaliable', ]


class ProductDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		# fields = '__all__'
		exclude = ['added_by']


### Order Serializers ###

class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'quantity', 'total_price', ]



class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'status', 'ordered_by', 'total_price', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','status', 'ordered_by', 'created_at', 'order_products']


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price']



## Order Product Serializers ##
class OrderProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['order', 'product', 'quantity']


class OrderProductQuantityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['quantity']

 
