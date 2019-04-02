from rest_framework.generics import CreateAPIView
from .serializers import (
    UserCreateSerializer,
    StatusListSerializer,
    StatusCreateUpdateSerializer
)
from .models import Status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
)



class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


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
