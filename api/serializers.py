from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Status

## MODELS ##
from .models import Product


class StatusListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name="api-detail",
        lookup_field="id",
        lookup_url_kwarg="status_id"
    )
    update = serializers.HyperlinkedIdentityField(
        view_name="api-update",
        lookup_field="id",
        lookup_url_kwarg="status_id"
    )

    class Meta:
        model = Status
        fields = ['title', 'is_active']


class StatusCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['title', 'is_active']
        

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
		# fields = '__all__'
		exclude = ['added_by']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		exclude = ['created_at', 'added_by']

