from django.contrib.auth.models import User
from rest_framework import serializers

## MODELS ##
from .models import Product


class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'password']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		return validated_data


class ProductListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
		view_name="products-detail",
		lookup_field="id",
		lookup_url_kwarg="product_id"
	)

	update = serializers.HyperlinkedIdentityField(
		view_name="products-update",
		lookup_field="id",
		lookup_url_kwarg="product_id"
	)

	class Meta:
		model = Product
		fields = ['id', 'detail', 'update', 'name',
				  'image', 'price', 'is_avaliable', ]


class ProductDetailSerializer(serializers.ModelSerializer):
	update = serializers.HyperlinkedIdentityField(
		view_name="products-update",
		lookup_field="id",
		lookup_url_kwarg="product_id"
	)

	class Meta:
		model = Product
		fields = '__all__'
		# exclude = ['added_by']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		exclude = ['created_at', 'added_by']