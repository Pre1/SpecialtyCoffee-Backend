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

# validate first_name, last_name in ProfileUpdateView
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
        # post save signal on user model
        new_profile = Profile(customer=new_user)
        new_profile.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(new_user)
        token = jwt_encode_handler(payload)
        validated_data['token'] = token
        return validated_data



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

# only need for adding options and variant to the product
# more efficient: making one request the list product api
class ProductDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		# fields = '__all__'
		exclude = ['added_by']


### Order Serializers ###

class OrderProductSerializer(serializers.ModelSerializer):

    # total_price = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'quantity', 'total_price', ]

    def get_product(self, obj):
        prod_id = obj.product.id
        prod_name = obj.product.name
        price = obj.product.price
        return {
            "id": prod_id,
            "name": prod_name,
            "price": price,
        }

    # def get_total_price(self, obj):
    #     return obj.get_price()


class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'status', 'ordered_by', 'total_price', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)
    status = StatusListSerializer()
    class Meta:
        model = Order
        fields = ['id','status', 'ordered_by', 'created_at', 'order_products', 'total_price']



class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price']



## Order Product Serializers ##
class OrderProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['order', 'product', 'quantity', 'total_price']


class OrderProductQuantityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['quantity']

 

class ProfileDetailSerializer(serializers.ModelSerializer):
    customer = UserSerializer()
    customer_orders = OrderDetailSerializer(many=True)
    class Meta:
        model = Profile
        fields = ['customer', 'image', 'customer_orders']


class ProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']