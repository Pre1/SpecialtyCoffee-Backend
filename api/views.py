from rest_framework.generics import (
CreateAPIView,
RetrieveUpdateAPIView,
RetrieveAPIView
)
from .serializers import (
UserCreateSerializer,  
ProfileDetailSerializer, 
ProfileCreateUpdateSerializer
)
from rest_framework.views import APIView
from .models import Profile
from django.contrib.auth.models import User

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
        
        profile = Profile.objects.get(id=pk)
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

