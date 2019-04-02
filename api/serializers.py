from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Status


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
