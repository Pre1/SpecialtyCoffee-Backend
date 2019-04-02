from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token= serializers.CharField(allow_blank=True, read_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'password','first_name','last_name','email', 'token',]

    def create(self, validated_data): 
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()

        # Saving the user to a new profile:
        new_profile = Profile(customer=new_user)
        new_profile.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(new_user)
        token = jwt_encode_handler(payload)
        validated_data['token']= token
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

    